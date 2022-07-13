"""Security feature tests."""

from pytest_bdd import (
    given,
    when,
    then,
    scenarios,
    scenario,
    parsers
)
import testinfra
import pytest

@scenario('security.feature',
          'Expect security updates to be installed')
def test_package_scenario():
    '''
    scenarios with tables that require type mapping must be referenced
    directly before calling "scenarios()"
    '''
    pass


scenarios('./')

@given(parsers.parse("the package {package} is installed"),
          converters=dict(package=str),
          target_fixture='package_is_installed')
def package_is_installed(host, package):
    assert host.package(package).is_installed
    return dict(package=package)


@given('the server is Ubuntu 14.04')
def the_server_is_ubuntu_1404(host):
    assert host.system_info.type == 'linux'
    assert host.system_info.distribution == 'arch' # 'Ubuntu'
    assert host.system_info.release == 'rolling' # '14.04'


@when('the server is running')
def the_nginx_server_is_running(host):
    """the ngingx server is running."""
    # assert host.service('nginx').is_running
    pass


@when('the version is fetched')
def the_version_is_fetched(host, package_is_installed):
    """the version is fetched."""
    version = host.package(package_is_installed['package']).version
    package_is_installed['version'] = version


@given('the server has a firewall installed')
def the_server_has_a_firewall_installed(host):
    """the server has a firewall installed."""
    # assert host.package('ufw').is_installed
    pass


@pytest.fixture(autouse=True)
@when('a list of open ports is fetched')
def a_list_of_open_ports_is_fetched(host):
    """a list of open ports is fetched."""
    return host.socket.get_listening_sockets()


@then(parsers.parse('the socks port {port:d} is not open'))
def the_socks_port_1080_is_not_open(a_list_of_open_ports_is_fetched, port):
    """the socks port 1080 is not open."""
    url = 'tcp://0.0.0.0:%d' % port
    assert url not in a_list_of_open_ports_is_fetched
    pass

# TODO: 'or later than' not working yet.
@then(parsers.parse("It should be equal or later than version {version}"),
          converters=dict(version=str),
          target_fixture='it_should_be_equal_or_later_than_version_version')
def it_should_be_equal_or_later_than_version_version(package_is_installed,
                                                     version):
    """It should be equal or later than version <version>."""
    assert package_is_installed['version'] == version
    pass