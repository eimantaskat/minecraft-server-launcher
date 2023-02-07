from PyQt5.QtCore import Qt


class ThreadHandler:
    """
    Class to manage threads
    """

    def __init__(self):
        self.threads = []


    def _start_thread(self, thread):
        """
        Run thread
        """
        self.threads.append(thread)
        thread.finished.connect(lambda: self.threads.remove(thread))
        thread.exception_raised.connect(
            self._handle_thread_exception, Qt.DirectConnection)
        thread.start()


    def add_thread(self, thread_class, *args, **kwargs):
        """
        Create and run new thread
        """
        thread = thread_class(*args, **kwargs)
        self._start_thread(thread)


    def stop_all_threads(self):
        """
        Stop all running threads
        """
        for thread in self.threads:
            thread.terminate()


    def get_running_threads(self):
        """
        Return a list of all running threads
        """
        running_threads = []
        for thread in self.threads:
            if thread.isRunning():
                running_threads.append(thread)
        return running_threads


    def stop_thread(self, thread):
        """
        Stop a specific thread
        """
        thread.terminate()


    def stop_threads_by_class(self, thread_class):
        """
        Stop all threads of a given class 
        """
        for thread in self.threads:
            if isinstance(thread, thread_class):
                thread.terminate()


    def is_thread_running(self, thread):
        """
        Check if a specific thread is running
        """
        return thread.isRunning()


    def wait_for_all_threads(self):
        """
        Wait for all threads to complete
        """
        for thread in self.threads:
            thread.wait()


    def get_threads_by_class(self, thread_class):
        """
        Return a list of running threads of a given class
        """
        threads = []
        for thread in self.threads:
            if isinstance(thread, thread_class):
                threads.append(thread)
        return threads


    def _handle_thread_exception(self, exception, message):
        # TODO handle exception
        print(message)
