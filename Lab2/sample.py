from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink


def runIperf(net, src, dst, bw_limit, duration=10):
    print("Starting iperf session from {} to {} with bandwidth limit {} Mbps".format(
        src, dst, bw_limit))
    # TODO (runIperf function)


def createTopo():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink)

    # TODO (Generate Topology)

    print("Starting network")
    net.start()

    # TODO (Set up iperf sessions)

    print("Running CLI")
    CLI(net)

    print("Stopping network")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    createTopo()
