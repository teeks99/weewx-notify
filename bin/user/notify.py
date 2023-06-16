from six.moves import queue
from six.moves import urllib
from six.moves.urllib import error as urlerror
import weewx
import weewx.restx
from weeutil.weeutil import accumulateLeaves

try:
    # Test for new-style weewx logging by trying to import weeutil.logger
    import weeutil.logger
    import logging
    log = logging.getLogger(__name__)

    def logdbg(msg):
        log.debug(msg)

    def loginf(msg):
        log.info(msg)

    def logerr(msg):
        log.error(msg)

except ImportError:
    # Old-style weewx logging
    import syslog

    def logmsg(level, msg):
        syslog.syslog(level, 'owm: %s' % msg)

    def logdbg(msg):
        logmsg(syslog.LOG_DEBUG, msg)

    def loginf(msg):
        logmsg(syslog.LOG_INFO, msg)

    def logerr(msg):
        logmsg(syslog.LOG_ERR, msg)

class Notify(weewx.restx.StdRESTbase):
    def __init__(self, engine, config_dict):
        super(Notify, self).__init__(engine, config_dict)

        url = ""
        try:
            site_dict = config_dict['StdRESTful']['Notify']
            site_dict = accumulateLeaves(site_dict, max_level=1)
            url = site_dict['url']
        except KeyError as e:
            logerr("Data will not be posted: Missing option %s" % e)
            return
        
        manager_dict = weewx.manager.get_manager_dict(
            config_dict['DataBindings'], config_dict['Databases'], 'wx_binding')
        
        self.archive_queue = queue.Queue()
        self.archive_thread = NotifyThread(self.archive_queue, manager_dict, url)
        self.archive_thread.start()

        self.bind(weewx.NEW_ARCHIVE_RECORD, self.new_archive_record)
        loginf("Notifications will be sent to: %s" % url)

    def new_archive_record(self, event):
        self.archive_queue.put(event.record)

class NotifyThread(weewx.restx.RESTThread):
    def __init__(self, queue, manager_dict,
                 url,
                 post_interval=None, max_backlog=0, stale=None,
                 log_success=True, log_failure=True,
                 timeout=60, max_tries=3, retry_wait=5):
        super(NotifyThread, self).__init__(queue,
                                                   protocol_name='Notify',
                                                   manager_dict=manager_dict,
                                                   post_interval=post_interval,
                                                   max_backlog=max_backlog,
                                                   stale=stale,
                                                   log_success=log_success,
                                                   log_failure=log_failure,
                                                   timeout=timeout,
                                                   max_tries=max_tries,
                                                   retry_wait=retry_wait)
        self.url = url

    def format_url(self, _):
        loginf("Notifying: %s" % self.url)
        return self.url
