pragma solidity >=0.4.21 <0.7.0;
contract Federation {

    enum ServiceState {Open, Closed, Deployed}
    struct Operator {
        bytes32 name;
        bool registered;
    }

    struct Service {
        address creator;
        bytes32 endpoint_consumer;
        bytes32 id;
        address provider;
        bytes32 endpoint_provider;
        bytes32 req_info;
        ServiceState state;
    }

    struct Bid {
        address bid_address;
        uint price;
        bytes32 endpoint_provider;
    }

    mapping(bytes32 => uint) public bidCount;
    mapping(bytes32 => Bid[]) public bids;
    mapping(bytes32 => Service) public service;
    mapping(address => Operator) public operator;

    event OperatorRegistered(address operator, bytes32 name);
    event ServiceAnnouncement(bytes32 requirements, bytes32 id);
    event NewBid(bytes32 _id, uint256 max_bid_index);
    event ServiceAnnouncementClosed(bytes32 _id);
    event ServiceDeployedEvent(bytes32 _id);

    function addOperator(bytes32 name) public {
        Operator storage current_operator = operator[msg.sender];
        require(name.length > 0, "Name is not valid");
        require(current_operator.registered == false, "Operator already registered");
        current_operator.name = name;
        current_operator.registered = true;
        emit OperatorRegistered(msg.sender, name);
    }

    function getOperatorInfo(address op_address) public view returns (bytes32 name) {
        Operator storage current_operator = operator[op_address];
        require(current_operator.registered == true, "Operator is not registered with this address. Please register.");
        return current_operator.name;
	}

    function AnnounceService(bytes32 _requirements, bytes32 _endpoint_consumer, bytes32 _id) public returns(ServiceState) {
        Operator storage current_operator = operator[msg.sender];
        Service storage current_service = service[_id];
        require(current_operator.registered == true, "Operator is not registered. Can not bid. Please register.");
        require(current_service.requirements == 0, "Service ID for operator already exists");

        service[_id] = Service(msg.sender, _endpoint_consumer, _id, msg.sender,  _endpoint_consumer, _requirements, ServiceState.Open);
        emit ServiceAnnouncement(_requirements, _id);
        return ServiceState.Open;
    }

    function GetServiceState(bytes32 _id) public view returns (ServiceState) {
        // Service storage current_service = service[_id];
        // require(service[_id].creator == _creator, "Service not exists");
        // assert(service[_id].state == ServiceState.Open);
        return service[_id].state;
    }

    function PlaceBid(bytes32 _id, uint32 _price, bytes32 _endpoint) public returns (uint256) {
        Operator storage current_operator = operator[msg.sender];
        Service storage current_service = service[_id];
        require(current_operator.registered == true, "Operator is not registered. Can not bid. Please register.");
        require(current_service.state == ServiceState.Open, "Service is closed or not exists");
        uint256 max_bid_index = bids[_id].push(Bid(msg.sender, _endpoint, _price));
        bidCount[_id] = max_bid_index;
        emit NewBid(_id, max_bid_index);
        return max_bid_index;
    }

    function GetBidCount(bytes32 _id, address _creator) public view returns (uint256) {
        Service storage current_service = service[_id];
        require(current_service.id == _id, "Service not exists");
        require(current_service.creator == _creator, "Only service creator can look into the information");
        return bidCount[_id];
    }

    function GetBids(bytes32 _id, uint256 bider_index, address _creator) public view returns (Bid[] bids) {
        Service storage current_service = service[_id];
        Bid[] storage current_bid_pool = bids[_id];
        require(current_service.id == _id, "Service not exists");
        require(current_service.creator == _creator, "Only service creator can look into the information");
        require(current_bid_pool.length > 0, "No bids for requested Service");
        // return (current_bid_pool[bider_index].bid_address, current_bid_pool[bider_index].price, bider_index);
        return bids[_id];
    }

    function ChooseProvider(bytes32 _id, uint256 bider_index) public returns (bytes32 endpoint_provider) {
        Service storage current_service = service[_id];
        Bid[] storage current_bid_pool = bids[_id];
        require(current_service.id == _id, "Service not exists");
        require(current_service.creator == msg.sender, "Only service creator can close the announcement");
        require(current_service.state == ServiceState.Open, "Service announcement already closed");

        current_service.state = ServiceState.Closed;
        // address bid_address_= current_bid_pool[bider_index].bid_address;
        service[_id].provider = current_bid_pool[bider_index].bid_address;
        service[_id].endpoint_provider = current_bid_pool[bider_index].endpoint_provider;
        emit ServiceAnnouncementClosed(_id);
        return service[_id].endpoint_provider;
        // return (current_bid_pool[bider_index].bid_address, current_bid_pool[bider_index].price);
    }

    function isWinner(bytes32 _id, address _winner) public view returns (bool) {
        Service storage current_service = service[_id];
        require(current_service.state == ServiceState.Closed, "Service winner not choosen. Service: DEPLOYED or OPEN");
        if(current_service.provider == _winner) {
            return true;
        }
        else {
            return false;
        }
    }

    function ServiceDeployed(bytes32 info, bytes32 _id) public returns (bool) {
        Service storage current_service = service[_id];
        require(current_service.id == _id, "Service not exists");
        require(current_service.provider == msg.sender, "Only service provider can deploy the service");
        require(current_service.state == ServiceState.Closed, "Service winner not choosen. Service: DEPLOYED or OPEN");
        current_service.state = ServiceState.Deployed;
        current_service.req_info = info;
        emit ServiceDeployedEvent(_id);
        return true;
    }


}