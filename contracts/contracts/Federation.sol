pragma solidity >=0.4.21 <0.7.0;
contract Federation {
    
    enum Location {Unregistered, Europe, Africa, Asia, NorthAmerica, SouthAmerica, Australia}
    enum ServiceState {Open, Closed}
    
    struct Operator {
        bytes32 name;
        Location location;
    }

    struct Service {
        address creator;
        uint32 requirements;
        Location[] locations;
        bytes32 id;
        ServiceState state;
    }

    struct Bider {
        address bid_address;
        uint price;
    } 

    mapping(bytes32 => uint) public bidCount;
    mapping(bytes32 => Bider[]) public biders;
    mapping(bytes32 => Service) public service;
    mapping(address => Operator) public operator;

    event OperatorRegistered(address operator, bytes32 name, Location location);
    event ServiceAnnouncement(uint32 requirements, Location[] location, bytes32 id);
    event NewBid(bytes32 _id, uint256 max_bid_index);
    event ServiceAnnouncementClosed(bytes32 _id, address bid_address_);

    function addOperator(bytes32 name, Location location) public {
        Operator storage current_operator = operator[msg.sender];
        require(name.length > 0, "Name is not valid");
        require(location <= Location.Australia);
        
        current_operator.name = name;
        current_operator.location = location;
        emit OperatorRegistered(msg.sender, name, location);
    }

    function getOperatorInfo(address op_address) public view returns (bytes32 name, Location location) {
        Operator storage current_operator = operator[op_address];
        require(current_operator.location > Location.Unregistered, "Operator is not registered with this address. Please register.");
        return (current_operator.name, current_operator.location);
	}

    function AnnounceService(uint32 _requirements, Location[] memory _location, bytes32 _id) public returns(ServiceState) {
        Operator storage current_operator = operator[msg.sender];
        Service storage current_service = service[_id];
        require(current_operator.location > Location.Unregistered, "Operator is not registered. Can not bid. Please register.");
        require(current_service.requirements == 0, "Service ID for operator already exists");

        service[_id] = Service(msg.sender, _requirements, _location, _id, ServiceState.Open);
        emit ServiceAnnouncement(_requirements, _location, _id);
        return ServiceState.Open;
    }

    function GetServiceAnnounce(bytes32 _id, address _creator) public view returns (address, uint32, Location[] memory, bytes32, ServiceState) {
        Service storage current_service = service[_id];
        require(service[_id].creator == _creator, "Service not exists");
        return (current_service.creator, current_service.requirements, current_service.locations, current_service.id, current_service.state);
    }

    function Bid(bytes32 _id, uint32 _price) public returns (uint256) {
        Operator storage current_operator = operator[msg.sender];
        Service storage current_service = service[_id];
        require(current_operator.location > Location.Unregistered, "Operator is not registered. Can not bid. Please register.");
        require(current_service.state == ServiceState.Open, "Service is closed or not exists");
        uint256 max_bid_index = biders[_id].push(Bider(msg.sender, _price));
        bidCount[_id] =  max_bid_index;
        emit NewBid(_id, max_bid_index);
        return max_bid_index;
    }

    function GetBidCount(bytes32 _id, address _creator) public view returns (uint256) {
        Service storage current_service = service[_id];
        require(current_service.id == _id, "Service not exists");
        require(current_service.creator == _creator, "Only service creator can look into the information");
        return bidCount[_id];
    }

    function GetBider(bytes32 _id, uint256 bider_index, address _creator) public view returns (address, uint, uint256) {
        Service storage current_service = service[_id];
        Bider[] storage current_bid_pool = biders[_id];
        require(current_service.id == _id, "Service not exists");
        require(current_service.creator == _creator, "Only service creator can look into the information");
        require(current_bid_pool.length > 0, "No bids for requested Service");
        return (current_bid_pool[bider_index].bid_address, current_bid_pool[bider_index].price, bider_index);
    }

    function CloseAnnounceService(bytes32 _id, uint256 bider_index) public returns (address, uint) {
        Service storage current_service = service[_id];
        Bider[] storage current_bid_pool = biders[_id];
        require(current_service.id == _id, "Service not exists");
        require(current_service.creator == msg.sender, "Only service creator can close the announcement");
        require(current_service.state == ServiceState.Open, "Service announcement already closed");

        current_service.state = ServiceState.Closed;
        address bid_address_= current_bid_pool[bider_index].bid_address;
        emit ServiceAnnouncementClosed(_id, bid_address_);
        return (current_bid_pool[bider_index].bid_address, current_bid_pool[bider_index].price);
    }
}