DLT Federation using Mininet simulations
=====
Scenario setup
-----

The configuration of the simulation:
1. 2 VMs containing mininet --> or two instances Mininet VM
2. Both interconnected through a host-only adapter of the host machine
3. Both Mininet VMs have access to a blockchain node

Idea
-----

The goal is to prove that they can establish federation efficiently using the DLT as a mediatior in the process. 
Both Mininet VMs act as separate administrative domains. 
At the start they do not have interconnection. 
At the end the domain that requests a federation, should have 100% control over a host in the other domain. 

Workflow
-----

1. Domain 1 and Domain 2 are instantiated
2. Mininet is started on both machines to symobolize that both administrative domains are up and running
3. Domain decides it needs additional host, requests federation to the DLT. 
4. The DLT broadcasts the request, Domain 2, accepts, bids and reveals its end-point
5. Domain 1, receives the bid offer, accepts and sends, its own end-point
6. Domain 1 uses the provided end-point and initializes a VXLAN interface to the Domain 2 end-point
7. Domain 2 deploys the host and creates a flow to the gateway, from the gateway creates a VXLAN to the Domain 1 end-point
8. When the new host is deployed, Domain 2, notifes Domain 1 on specified IP address