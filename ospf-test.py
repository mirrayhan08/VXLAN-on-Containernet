#!/usr/bin/python
from mininet.net import Containernet
from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host
from mininet.node import Node
from mininet.node import OVSKernelSwitch, UserSwitch, OVSSwitch
from mininet.node import IVSSwitch
from mininet.log import setLogLevel, info
from mininet.cli import CLI
from mininet.link import Link, TCLink
import time
import glob, os

# Configure the router's IPV4 forwarding
class LinuxRouter( Node ):
    "A Node with IP forwarding enabled."

    def config( self, **params ):
        super( LinuxRouter, self).config( **params )
        # Enable
        self.cmd( 'sysctl net.ipv4.ip_forward=1' )

    def terminate( self ):
         # Disable
        self.cmd( 'sysctl net.ipv4.ip_forward=0' )
        super( LinuxRouter, self ).terminate()


class ospfTopo():
    # Add the Container net and define the switch category
    net = Containernet( controller=Controller, link=TCLink, switch=OVSKernelSwitch )
    info('Adding controller\n')
    c0 = net.addController( name='c0', controller=Controller, ip='127.0.0.1', protocol='tcp', port=6633 )
    
    #Define Hosts
    
    # Define DHCP Servers
    d3 = net.addDocker( name='d3', ip='192.168.1.10/24', defaultRoute='via 192.168.1.1', dimage="dhcp1", mac="04:a3:82:14:30:31")
    
    h1 = net.addDocker( name='h1',  ip='192.168.1.100/24', defaultRoute='via 192.168.1.1', dimage='host1', mac="24:ec:5d:83:b1:5d")
    h2 = net.addHost( name='h2', ip='192.168.1.200/24', defaultRoute='via 192.168.1.1', mac="ca:8b:28:0d:63:d5")
    
    #=============== Host 2 IP Renew =======
    #h2.cmd("dhclient -r h2-eth0")
    #h2.cmd("dhclient h2-eth0")
    #================= End ================= 
    
    h3 = net.addDocker( name='h3', ip='192.168.2.100/24', defaultRoute='via 192.168.2.1', dimage='host', mac="95:0e:5e:de:70:e9")
    h4 = net.addHost( name='h4', ip='192.168.2.200/24', defaultRoute='via 192.168.2.1', mac="5e:dc:11:8f:e0:5d")
    
    # Define Call Servers
    d1 = net.addDocker( name='d1', ip='192.168.3.100/24', defaultRoute='via 192.168.3.1', dimage="callserver", mac="04:a3:82:14:20:31")
    
    # Define File Server
    d2 = net.addDocker( name='d2', ip='192.168.3.200/24', defaultRoute='via 192.168.3.1', dimage="vsftp1", mac="00:00:00:00:01:01")
    
    #Define switches
    
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s3 = net.addSwitch('s3', cls=OVSKernelSwitch)
    
    #Define Routers
    r1 = net.addHost( 'r1', cls=LinuxRouter, ip='10.10.10.1/30' )
    r2 = net.addHost( 'r2', cls=LinuxRouter, ip='20.20.20.1/30' )
    r3 = net.addHost( 'r3', cls=LinuxRouter, ip='100.10.1.2/30' )
    r4 = net.addHost( 'r4', cls=LinuxRouter, ip='101.20.1.2/30' )
    r5 = net.addHost( 'r5', cls=LinuxRouter, ip='116.170.1.1/30' )
    r6 = net.addHost( 'r6', cls=LinuxRouter, ip='117.180.1.1/30' )
    r7 = net.addHost( 'r7', cls=LinuxRouter, ip='103.40.1.2/30' )
    r8 = net.addHost( 'r8', cls=LinuxRouter, ip='104.50.1.2/30' )
    r9 = net.addHost( 'r9', cls=LinuxRouter, ip='105.60.1.2/30' )
    r10 = net.addHost( 'r10', cls=LinuxRouter, ip='114.150.1.1/30' )
    r11 = net.addHost( 'r11', cls=LinuxRouter, ip='107.80.1.2/30' )
    r12 = net.addHost( 'r12', cls=LinuxRouter, ip='192.168.1.1/24' )
    r13 = net.addHost( 'r13', cls=LinuxRouter, ip='192.168.2.1/24' )
    r14 = net.addHost( 'r14', cls=LinuxRouter, ip='192.168.3.1/24' )

    #Define Host to Switch Links
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s1, d3)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    net.addLink(s3, d1)
    net.addLink(s3, d2)

    # #Define Switch to Router Links
    net.addLink(s1,r12,intfName2='r12-eth0',params2={ 'ip' : '192.168.1.1/24' })
    net.addLink(s2,r13,intfName2='r13-eth0',params2={ 'ip' : '192.168.2.1/24' })
    net.addLink(s3,r14,intfName2='r14-eth0',params2={ 'ip' : '192.168.3.1/24' })

   #Define Router to Router Links
    net.addLink(r1,r12,intfName1='r1-eth0',intfName2='r12-eth1',params1={ 'ip' : '10.10.10.1/30' },params2={ 'ip' : '10.10.10.2/30' })
    net.addLink(r1,r3,intfName1='r1-eth1',intfName2='r3-eth0',params1={ 'ip' : '100.10.1.1/30' },params2={ 'ip' : '100.10.1.2/30' })
    net.addLink(r1,r4,intfName1='r1-eth2',intfName2='r4-eth0',params1={ 'ip' : '101.20.1.1/30' },params2={ 'ip' : '101.20.1.2/30' })
    net.addLink(r3,r4,intfName1='r3-eth1',intfName2='r4-eth1',params1={ 'ip' : '102.30.1.1/30' },params2={ 'ip' : '102.30.1.2/30' })
    net.addLink(r3,r7,intfName1='r3-eth2',intfName2='r7-eth0',params1={ 'ip' : '103.40.1.1/30' },params2={ 'ip' : '103.40.1.2/30' })
    net.addLink(r4,r8,intfName1='r4-eth2',intfName2='r8-eth0',params1={ 'ip' : '104.50.1.1/30' },params2={ 'ip' : '104.50.1.2/30' })
    net.addLink(r4,r9,intfName1='r4-eth3',intfName2='r9-eth0',params1={ 'ip' : '105.60.1.1/30' },params2={ 'ip' : '105.60.1.2/30' })
    net.addLink(r7,r8,intfName1='r7-eth1',intfName2='r8-eth1',params1={ 'ip' : '106.70.1.1/30' },params2={ 'ip' : '106.70.1.2/30' })
    net.addLink(r7,r11,intfName1='r7-eth2',intfName2='r11-eth0',params1={ 'ip' : '107.80.1.1/30' },params2={ 'ip' : '107.80.1.2/30' })
    
    net.addLink(r8,r11,intfName1='r8-eth3',intfName2='r11-eth1',params1={ 'ip' : '109.100.1.1/30' },params2={ 'ip' : '109.100.1.2/30' })
    net.addLink(r11,r9,intfName1='r11-eth2',intfName2='r9-eth3',params1={ 'ip' : '110.100.1.1/30' },params2={ 'ip' : '110.110.1.2/30' })
    net.addLink(r9,r10,intfName1='r9-eth2',intfName2='r10-eth1',params1={ 'ip' : '112.130.1.1/30' },params2={ 'ip' : '112.130.1.2/30' })
    net.addLink(r11,r10,intfName1='r11-eth3',intfName2='r10-eth2',params1={ 'ip' : '111.120.1.1/30' },params2={ 'ip' : '111.120.1.2/30' })
    
    net.addLink(r2,r13,intfName1='r2-eth0',intfName2='r13-eth1',params1={ 'ip' : '20.20.20.1/30' },params2={ 'ip' : '20.20.20.2/30' })
    net.addLink(r5,r2,intfName1='r5-eth0',intfName2='r2-eth1',params1={ 'ip' : '116.170.1.1/30' },params2={ 'ip' : '116.170.1.2/30' })
    net.addLink(r6,r2,intfName1='r6-eth0',intfName2='r2-eth2',params1={ 'ip' : '117.180.1.1/30' },params2={ 'ip' : '117.180.1.2/30' })      
    net.addLink(r5,r6,intfName1='r5-eth1',intfName2='r6-eth1',params1={ 'ip' : '115.160.1.1/30' },params2={ 'ip' : '115.160.1.2/30' })
    net.addLink(r8,r5,intfName1='r8-eth2',intfName2='r5-eth2',params1={ 'ip' : '108.90.1.1/30' },params2={ 'ip' : '108.90.1.2/30' })
    net.addLink(r9,r5,intfName1='r9-eth1',intfName2='r5-eth3',params1={ 'ip' : '113.140.1.1/30' },params2={ 'ip' : '113.140.1.2/30' })
    net.addLink(r10,r6,intfName1='r10-eth0',intfName2='r6-eth2',params1={ 'ip' : '114.150.1.1/30' },params2={ 'ip' : '114.150.1.2/30' })
    net.addLink(r11,r14,intfName1='r11-eth4',intfName2='r14-eth1',params1={ 'ip' : '150.50.50.1/30' },params2={ 'ip' : '150.50.50.2/30' })
    
    # Define the node name
    info( '*** Routing Table on Router:\n' )
    s1=net.getNodeByName('s1')
    s2=net.getNodeByName('s2')
    s3=net.getNodeByName('s3')

    r1=net.getNodeByName('r1')
    r2=net.getNodeByName('r2')
    r3=net.getNodeByName('r3')
    r4=net.getNodeByName('r4')
    r5=net.getNodeByName('r5')
    r6=net.getNodeByName('r6')
    r7=net.getNodeByName('r7')
    r8=net.getNodeByName('r8')
    r9=net.getNodeByName('r9')
    r10=net.getNodeByName('r10')
    r11=net.getNodeByName('r11')
    r12=net.getNodeByName('r12')
    r13=net.getNodeByName('r13')
    r14=net.getNodeByName('r14')
    info('starting zebra and ospfd service:\n')
    
    net.build()
    # Start the Controller 
    c0.start
    s1.start( [c0] )
    s2.start( [c0] )
    s3.start( [c0] )
    
    # # Adding MAC on the router interface
    info(net['r12'].cmd("ifconfig r12-eth0 hw ether 46:00:43:2c:b0:9e"))
    info(net['r13'].cmd("ifconfig r13-eth0 hw ether 00:00:00:00:00:01")) 
    info(net['r14'].cmd("ifconfig r14-eth0 hw ether 00:00:00:00:00:04")) 
    
    #Create the rotuer APIs
    r1.cmd('zebra -f /usr/local/etc/mininet/r1zebra.conf -d -z /usr/local/etc/mininet/r1zebra.api -i /usr/local/etc/mininet/r1zebra.interface') 
    r2.cmd('zebra -f /usr/local/etc/mininet/r2zebra.conf -d -z /usr/local/etc/mininet/r2zebra.api -i /usr/local/etc/mininet/r2zebra.interface')
    r3.cmd('zebra -f /usr/local/etc/mininet/r3zebra.conf -d -z /usr/local/etc/mininet/r3zebra.api -i /usr/local/etc/mininet/r3zebra.interface')
    r4.cmd('zebra -f /usr/local/etc/mininet/r4zebra.conf -d -z /usr/local/etc/mininet/r4zebra.api -i /usr/local/etc/mininet/r4zebra.interface')
    r5.cmd('zebra -f /usr/local/etc/mininet/r5zebra.conf -d -z /usr/local/etc/mininet/r5zebra.api -i /usr/local/etc/mininet/r5zebra.interface')
    r6.cmd('zebra -f /usr/local/etc/mininet/r6zebra.conf -d -z /usr/local/etc/mininet/r6zebra.api -i /usr/local/etc/mininet/r6zebra.interface')
    r7.cmd('zebra -f /usr/local/etc/mininet/r7zebra.conf -d -z /usr/local/etc/mininet/r7zebra.api -i /usr/local/etc/mininet/r7zebra.interface')
    r8.cmd('zebra -f /usr/local/etc/mininet/r8zebra.conf -d -z /usr/local/etc/mininet/r8zebra.api -i /usr/local/etc/mininet/r8zebra.interface')
    r9.cmd('zebra -f /usr/local/etc/mininet/r9zebra.conf -d -z /usr/local/etc/mininet/r9zebra.api -i /usr/local/etc/mininet/r9zebra.interface')
    r10.cmd('zebra -f /usr/local/etc/mininet/r10zebra.conf -d -z /usr/local/etc/mininet/r10zebra.api -i /usr/local/etc/mininet/r10zebra.interface')
    r11.cmd('zebra -f /usr/local/etc/mininet/r11zebra.conf -d -z /usr/local/etc/mininet/r11zebra.api -i /usr/local/etc/mininet/r11zebra.interface')
    r12.cmd('zebra -f /usr/local/etc/mininet/r12zebra.conf -d -z /usr/local/etc/mininet/r12zebra.api -i /usr/local/etc/mininet/r12zebra.interface')
    r13.cmd('zebra -f /usr/local/etc/mininet/r13zebra.conf -d -z /usr/local/etc/mininet/r13zebra.api -i /usr/local/etc/mininet/r13zebra.interface')
    r14.cmd('zebra -f /usr/local/etc/mininet/r14zebra.conf -d -z /usr/local/etc/mininet/r14zebra.api -i /usr/local/etc/mininet/r14zebra.interface')
    
    #Create the OSPF interfaces
    r1.cmd('ospfd -f /usr/local/etc/mininet/r1ospfd.conf -d -z /usr/local/etc/mininet/r1zebra.api -i /usr/local/etc/mininet/r1ospfd.interface')
    r2.cmd('ospfd -f /usr/local/etc/mininet/r2ospfd.conf -d -z /usr/local/etc/mininet/r2zebra.api -i /usr/local/etc/mininet/r2ospfd.interface')
    r3.cmd('ospfd -f /usr/local/etc/mininet/r3ospfd.conf -d -z /usr/local/etc/mininet/r3zebra.api -i /usr/local/etc/mininet/r3ospfd.interface')
    r4.cmd('ospfd -f /usr/local/etc/mininet/r4ospfd.conf -d -z /usr/local/etc/mininet/r4zebra.api -i /usr/local/etc/mininet/r4ospfd.interface')
    r5.cmd('ospfd -f /usr/local/etc/mininet/r5ospfd.conf -d -z /usr/local/etc/mininet/r5zebra.api -i /usr/local/etc/mininet/r5ospfd.interface')
    r6.cmd('ospfd -f /usr/local/etc/mininet/r6ospfd.conf -d -z /usr/local/etc/mininet/r6zebra.api -i /usr/local/etc/mininet/r6ospfd.interface')
    r7.cmd('ospfd -f /usr/local/etc/mininet/r7ospfd.conf -d -z /usr/local/etc/mininet/r7zebra.api -i /usr/local/etc/mininet/r7ospfd.interface')
    r8.cmd('ospfd -f /usr/local/etc/mininet/r8ospfd.conf -d -z /usr/local/etc/mininet/r8zebra.api -i /usr/local/etc/mininet/r8ospfd.interface')
    r9.cmd('ospfd -f /usr/local/etc/mininet/r9ospfd.conf -d -z /usr/local/etc/mininet/r9zebra.api -i /usr/local/etc/mininet/r9ospfd.interface')
    r10.cmd('ospfd -f /usr/local/etc/mininet/r10ospfd.conf -d -z /usr/local/etc/mininet/r10zebra.api -i /usr/local/etc/mininet/r10ospfd.interface')
    r11.cmd('ospfd -f /usr/local/etc/mininet/r11ospfd.conf -d -z /usr/local/etc/mininet/r11zebra.api -i /usr/local/etc/mininet/r11ospfd.interface')
    r12.cmd('ospfd -f /usr/local/etc/mininet/r12ospfd.conf -d -z /usr/local/etc/mininet/r12zebra.api -i /usr/local/etc/mininet/r12ospfd.interface')
    r13.cmd('ospfd -f /usr/local/etc/mininet/r13ospfd.conf -d -z /usr/local/etc/mininet/r13zebra.api -i /usr/local/etc/mininet/r13ospfd.interface')
    r14.cmd('ospfd -f /usr/local/etc/mininet/r14ospfd.conf -d -z /usr/local/etc/mininet/r14zebra.api -i /usr/local/etc/mininet/r14ospfd.interface')
    
    #Allow time to create the interfaces
    time.sleep(15)
    
    #====================== OVS Forwarding ====================
    
    info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=1,arp,actions=flood"))
    info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=65535,ip,dl_dst=46:00:43:2c:b0:9e,actions=output:4"))
    info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_dst=192.168.1.10,actions=output:3"))    
    info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=192.168.1.10,nw_dst=192.168.1.200,actions=output:2"))
    
    info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=192.168.2.100,nw_dst=192.168.1.100,actions=output:1"))
    info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=192.168.3.100,nw_dst=192.168.1.100,actions=output:1"))
    info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=192.168.2.200,nw_dst=192.168.1.200,actions=output:2"))
    info(net['s1'].cmd("ovs-ofctl add-flow s1 priority=10,ip,nw_src=192.168.3.200,nw_dst=192.168.1.200,actions=output:2"))

    info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=1,arp,actions=flood"))
    info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=65535,ip,dl_dst=00:00:00:00:00:01,actions=output:3"))
    info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=192.168.1.100,nw_dst=192.168.2.100,actions=output:1"))
    info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=192.168.3.100,nw_dst=192.168.2.100,actions=output:1"))
    info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=192.168.1.200,nw_dst=192.168.2.200,actions=output:2"))
    info(net['s2'].cmd("ovs-ofctl add-flow s2 priority=10,ip,nw_src=192.168.3.200,nw_dst=192.168.2.200,actions=output:2"))
    
    info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=1,arp,actions=flood"))
    info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=65535,ip,dl_dst=00:00:00:00:00:04,actions=output:3"))
    info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=10,ip,nw_src=192.168.1.100,nw_dst=192.168.3.100,actions=output:1"))
    info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=10,ip,nw_src=192.168.2.100,nw_dst=192.168.3.100,actions=output:1"))
    info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=10,ip,nw_src=192.168.1.200,nw_dst=192.168.3.200,actions=output:2"))
    info(net['s3'].cmd("ovs-ofctl add-flow s3 priority=10,ip,nw_src=192.168.2.200,nw_dst=192.168.3.200,actions=output:2"))
    
    #====================== OVS Forwarding END ================
    
    #=============== VXLAN On Linux ================

    # For Router 12-13 VXLAN 1-2
    r12.cmd ('ip link add vxlan1 type vxlan id 1 remote 20.20.20.2 dstport 4789 dev r12-eth1') 
    r12.cmd ('ip link add vxlan2 type vxlan id 2 remote 20.20.20.2 dstport 4789 dev r12-eth1')
    r13.cmd ('ip link add vxlan1 type vxlan id 1 remote 10.10.10.2 dstport 4789 dev r13-eth1') 
    r13.cmd ('ip link add vxlan2 type vxlan id 2 remote 10.10.10.2 dstport 4789 dev r13-eth1')
    
    # For Router 12-14 VXLAN 1-2
    r12.cmd ('ip link add vxlan3 type vxlan id 3 remote 150.50.50.2 dstport 4789 dev r12-eth1')  
    r12.cmd ('ip link add vxlan4 type vxlan id 4 remote 150.50.50.2 dstport 4789 dev r12-eth1')
    r14.cmd ('ip link add vxlan3 type vxlan id 3 remote 10.10.10.2 dstport 4789 dev r14-eth1') 
    r14.cmd ('ip link add vxlan4 type vxlan id 4 remote 10.10.10.2 dstport 4789 dev r14-eth1')
    
    # For Router 13-14 VXLAN 1-2
    r13.cmd ('ip link add vxlan5 type vxlan id 5 remote 150.50.50.2 dstport 4789 dev r13-eth1')
    r13.cmd ('ip link add vxlan6 type vxlan id 6 remote 150.50.50.2 dstport 4789 dev r13-eth1') 
    r14.cmd ('ip link add vxlan5 type vxlan id 5 remote 20.20.20.2 dstport 4789 dev r14-eth1')
    r14.cmd ('ip link add vxlan6 type vxlan id 6 remote 20.20.20.2 dstport 4789 dev r14-eth1') 
    
    # For Router 12-13 VXLAN 1-2
    r12.cmd ('ip link set vxlan1 up')
    r12.cmd ('ip addr add 10.0.0.1/30 dev vxlan1') 
    r12.cmd ('ip link set vxlan2 up')
    r12.cmd ('ip addr add 20.0.0.1/30 dev vxlan2')
    r13.cmd ('ip link set vxlan1 up')
    r13.cmd ('ip addr add 10.0.0.2/30 dev vxlan1')  
    r13.cmd ('ip link set vxlan2 up')
    r13.cmd ('ip addr add 20.0.0.2/30 dev vxlan2')  
    
    # For Router 12-14 VXLAN 3-4
    r12.cmd ('ip link set vxlan3 up')
    r12.cmd ('ip addr add 30.0.0.1/30 dev vxlan3')
    r12.cmd ('ip link set vxlan4 up')
    r12.cmd ('ip addr add 40.0.0.1/30 dev vxlan4')
    r14.cmd ('ip link set vxlan3 up')
    r14.cmd ('ip addr add 30.0.0.2/30 dev vxlan3')
    r14.cmd ('ip link set vxlan4 up')
    r14.cmd ('ip addr add 40.0.0.2/30 dev vxlan4') 
    
    # For Router 13-14 VXLAN 5-6
    r13.cmd ('ip link set vxlan5 up')
    r13.cmd ('ip addr add 50.0.0.1/30 dev vxlan5')
    r13.cmd ('ip link set vxlan6 up')
    r13.cmd ('ip addr add 60.0.0.1/30 dev vxlan6')
    r14.cmd ('ip link set vxlan5 up')
    r14.cmd ('ip addr add 50.0.0.2/30 dev vxlan5')
    r14.cmd ('ip link set vxlan6 up')
    r14.cmd ('ip addr add 60.0.0.2/30 dev vxlan6') 
      
    # VXLAN Static Route
    r12.cmd('ip route add 192.168.2.100/32 via 10.0.0.2 encap ip  dev vxlan1')
    r12.cmd('ip route add 192.168.3.100/32 via 30.0.0.2 encap ip  dev vxlan3')
    r12.cmd('ip route add 192.168.2.200/32 via 20.0.0.2 encap ip  dev vxlan2')
    r12.cmd('ip route add 192.168.3.200/32 via 40.0.0.2 encap ip  dev vxlan4')
    
    r13.cmd('ip route add 192.168.1.100/32 via 10.0.0.1 encap ip  dev vxlan1') 
    r13.cmd('ip route add 192.168.3.100/32 via 50.0.0.2 encap ip  dev vxlan5')
    r13.cmd('ip route add 192.168.1.200/32 via 20.0.0.1 encap ip  dev vxlan2')
    r13.cmd('ip route add 192.168.3.200/32 via 60.0.0.2 encap ip  dev vxlan6')
    
    r14.cmd('ip route add 192.168.1.100/32 via 30.0.0.1 encap ip  dev vxlan3')
    r14.cmd('ip route add 192.168.2.100/32 via 50.0.0.1 encap ip  dev vxlan5')
    r14.cmd('ip route add 192.168.1.200/32 via 40.0.0.1 encap ip  dev vxlan4')
    r14.cmd('ip route add 192.168.2.200/32 via 60.0.0.1 encap ip  dev vxlan6')  
    
    #=============== End ================
    
    CLI( net )
    net.stop()
    os.system("killall -9 ospfra")
    os.system("rm -f /usr/local/etc/mininet/*api*")
    os.system("rm -f /usr/local/etc/mininet/*interface*")
    os.system("/etc/init.d/quagga restart")
    os.system("ifconfig vxlan_sys_4789 down")

    # Stop and delete running dockers
    os.system("docker stop $(docker ps -a -q)")
    os.system("docker rm $(docker ps -a -q)")
    #os.system("service networking restart")
    
    # Clean the mininet enviroment
    os.system("mn -c")

if __name__=='__main__':
    setLogLevel( 'info' )
    ospfTopo()
