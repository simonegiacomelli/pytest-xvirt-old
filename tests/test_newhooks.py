import pytest


def test_collection_finish(pytester: pytest.Pytester) -> None:
    pytester.makeconftest(
        f"""
        def pytest_xvirt_controlled_send_event(event):
            from xvirt.events import EvtCollectionFinish
            if isinstance(event, EvtCollectionFinish): 
                stripped_ids = [x.split('::')[1] for x in event.node_ids]
                print(f'HOOK: ' + ', '.join(stripped_ids))
    """
    )
    pytester.makepyfile(
        """
        import os
        def test_a(): pass
        def test_b(): pass
        def test_c(): pass
    """
    )
    # pytester.runpytest_inprocess(f'--xvirt-remote-transport={remote_transport}')
    res = pytester.runpytest()  # f'--xvirt-mode=controlled')
    res.stdout.fnmatch_lines_random(["*HOOK: test_a, test_b, test_c"])
