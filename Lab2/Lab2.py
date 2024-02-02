from mininet.net import Mininet
from mininet.node import OVSSwitch, RemoteController
from mininet.cli import CLI
from mininet.log import setLogLevel
from mininet.link import TCLink


def runIperf(net, src, dst, bw_limit, duration=10):
    print("Starting iperf session from {} to {} with bandwidth limit {} Mbps".format(
        src, dst, bw_limit))
    # TODO (runIperf function)
    #result = net.monitor([src, dst])                                                   # Unable to print out
    #dst.pexec(f"iperf -s &")                                                           # this one does not work
    #dst.cmd(f"iperf -s &")                                                             # this also works, will not stop client host after entering CLI
    #dst.sendCmd(f"iperf -s")                                                           # Send a command, return without waiting for the command to complete. This one will stop client host somehow, should be fine?
    #dst.cmd("iperf -s -D -P 1")                                                        # Open iperf server in daemon mode, close after 1 connection ends
    dst.cmd("iperf -s -D")                                                              # Open iperf server in daemon mode
    #src.cmdPrint(f"iperf -c {dst.IP()} -b {bw_limit}m -t {duration}")                  # Call cmd and printing its output. This will print out extra line containing the command you give to cmd
    output = src.cmd(f"iperf -c {dst.IP()} -b {bw_limit}m -t {duration}")
    print(output)                                                         
    #src.sendCmd(f"iperf -c {dst.IP()} -b {bw_limit}m -t {duration}")                   # Not work for client due to 'assert self.shell and not self.waiting' assertion error
    #net.iperf(hosts = [dst, src], udpBw = str(bw_limit) + 'M', seconds = duration)
    lines = output.splitlines()
    for line in lines:
        if 'Mbits/sec' in line:
            bandwidth_value = line.split()[-2]                                          # Assuming the bandwidth value is the second-to-last element
            if float(bandwidth_value) > bw_limit:
                #print("Exceeded")
                dst.cmd("pkill iperf")                                                  # kill the iperf server process
                src.cmd("pkill iperf")                                                  # kill the iperf client process, this should not be necessary since client will automatically shutdown after 10sec
            break
    #print("Bandwidth (bps):", result)

def createTopo():
    net = Mininet(controller=None, switch=OVSSwitch, link=TCLink)

    # TODO (Generate Topology)
    #c1 = net.addController('c1',ip='127.0.0.1', port=8080)
    c1 = net.addController('c1', controller = RemoteController)
    #c1 = net.addController('c1', controller = "ryu.app.simple_switch")

    #Error if not specified MAC
    h1 = net.addHost('h1', mac='00:00:00:00:00:01', ip = '10.0.0.1')
    h2 = net.addHost('h2', mac='00:00:00:00:00:02', ip = '10.0.0.2')
    h3 = net.addHost('h3', mac='00:00:00:00:00:03', ip = '10.0.0.3')
    h4 = net.addHost('h4', mac='00:00:00:00:00:04', ip = '10.0.0.4')
    h5 = net.addHost('h5', mac='00:00:00:00:00:05', ip = '10.0.0.5')
    h6 = net.addHost('h6', mac='00:00:00:00:00:06', ip = '10.0.0.6')
    h7 = net.addHost('h7', mac='00:00:00:00:00:07', ip = '10.0.0.7')
    h8 = net.addHost('h8', mac='00:00:00:00:00:08', ip = '10.0.0.8')
    h9 = net.addHost('h9', mac='00:00:00:00:00:09', ip = '10.0.0.9')
    
    s1 = net.addSwitch('s1')
    s2 = net.addSwitch('s2')
    s3 = net.addSwitch('s3')
    s4 = net.addSwitch('s4')
    s5 = net.addSwitch('s5')
    s6 = net.addSwitch('s6')
    #port1 indicate which port to use for the first node provides
    net.addLink(h1, s1, port1 = 1, port2 = 1)
    net.addLink(h2, s1, port1 = 1, port2 = 2)
    net.addLink(s1, s2, port1 = 3, port2 = 1)
    net.addLink(s2, h3, port1 = 2, port2 = 1)
    net.addLink(s2, s3, port1 = 3, port2 = 1)
    net.addLink(s3, h4, port1 = 2, port2 = 1)
    net.addLink(s3, h5, port1 = 3, port2 = 1)
    net.addLink(s1, s4, port1 = 4, port2 = 1)
    net.addLink(s4, h6, port1 = 2, port2 = 1)
    net.addLink(s4, s5, port1 = 3, port2 = 1)
    net.addLink(s5, h7, port1 = 2, port2 = 1)
    net.addLink(s5, s6, port1 = 3, port2 = 1)
    net.addLink(s6, h8, port1 = 2, port2 = 1)
    net.addLink(s6, h9, port1 = 3, port2 = 1)

    print("Starting network")
    net.start()

    # TODO (Set up iperf sessions)

    #net.startTerms()
    #h1 = net.get('h1')
    #print(h1.IP())
    
    runIperf(net, h1, h2, 5)
    runIperf(net, h1, h3, 10)
    runIperf(net, h4, h5, 15)
    runIperf(net, h6, h8, 20)
    
    print("Running CLI")
    CLI(net)

    print("Stopping network")
    net.stop()


if __name__ == '__main__':
    setLogLevel('info')
    createTopo()
