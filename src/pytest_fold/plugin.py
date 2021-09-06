from _pytest.pathlib import Path
import pytest
import curses


def pytest_addoption(parser):
    group = parser.getgroup("console folding", "console-fold plugin options")
    group.addoption(
        "--console-fold",
        action="store",
        metavar="path",
        default=None,
        help="Fold/unfold console output for failed tests.",
    )


def pytest_configure(config):
    console_fold = config.option.console_fold
    if console_fold and not hasattr(config, "workerinput"):
        config._console_fold_plugin = ConsoleFoldPlugin(config, Path(console_fold))
        config.pluginmanager.register(config._console_fold_plugin)


def pytest_unconfigure(config):
    console_fold_plugin = getattr(config, "_console_fold_plugin", None)
    if console_fold_plugin:
        console_fold_plugin.close()
        del config._console_fold_plugin


# @pytest.fixture(scope='session', autouse=True)
@pytest.fixture(scope='session')
def session_setup_teardown():
    print("setup session")
    breakpoint()
    yield
    print("teardown session")
    breakpoint()
    # pytest_fold.main()
    breakpoint()


class ConsoleFoldPlugin:
    def __init__(self, config):
        self._config = config

    def pytest_sessionstart(self):
        self.start_data = {
            "pytest_version": pytest.__version__,
            "$report_type": "SessionStart",
        }

    def pytest_sessionfinish(self, exitstatus):
        self.finish_data = {"exitstatus": exitstatus, "$report_type": "SessionFinish"}

    def pytest_runtest_logreport(self, report):
        self.runtest_logreport_data = self._config.hook.pytest_report_to_serializable(
            config=self._config, report=report
        )
        yield
        if report.when == "call" and report.failed:
            if report.session.config.option.fold:
                report.longrepr.chain[0][0].reprentries[0].lines.insert(0, "▶ ▼\n")
                report.longrepr.chain[0][0].extraline = "◀ ▲"

    def pytest_collectreport(self, report):
        self.collectreport_data = self._config.hook.pytest_report_to_serializable(
            config=self._config, report=report
        )

    def pytest_terminal_summary(self, terminalreporter):
        terminalreporter.write_sep(
            "-",
            f"self.start_data: {self.start_data}"
            f"self.finish_data: {self.start_data}",
            f"self.runtest_logreport_data: {self.runtest_logreport_data}",
            f"self.collectreport_data: {self.collectreport_data}",
        )

    def post_process_data(self):
        stdscr = curses.initscr()
