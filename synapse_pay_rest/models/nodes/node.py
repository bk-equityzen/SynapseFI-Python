from synapse_pay_rest.models.users.user import User
from .ach_us_node import AchUsNode
from .eft_ind_node import EftIndNode
from .eft_np_node import EftNpNode
from .iou_node import IouNode
from .reserve_us_node import ReserveUsNode
from .synapse_ind_node import SynapseIndNode
from .synapse_np_node import SynapseNpNode
from .synapse_us_node import SynapseUsNode
from .wire_int_node import WireIntNode
from .wire_us_node import WireUsNode


class Node():
    """ Factory for producing the various node types, which descend from
    BaseNode.
    """

    NODE_TYPES_TO_CLASSES = {
      'ACH-US': AchUsNode,
      'EFT-NP': EftNpNode,
      'EFT-IND': EftIndNode,
      'IOU': IouNode,
      'RESERVE-US': ReserveUsNode,
      'SYNAPSE-IND': SynapseIndNode,
      'SYNAPSE-NP': SynapseNpNode,
      'SYNAPSE-US': SynapseUsNode,
      'WIRE-INT': WireIntNode,
      'WIRE-US': WireUsNode
    }

    @classmethod
    def from_response(cls, user, response):
        args = {
          'user': user,
          'type': response.get('type'),
          'id': response.get('_id'),
          'is_active': response.get('is_active'),
          'permission': response.get('allowed'),
          'nickname': response['info'].get('nickname'),
          'name_on_account': response['info'].get('name_on_account'),
          'bank_long_name': response['info'].get('bank_long_name'),
          'bank_name': response['info'].get('bank_name'),
          'account_type': response['info'].get('type'),
          'account_class': response['info'].get('class'),
          'account_number': response['info'].get('account_num'),
          'routing_number': response['info'].get('routing_num'),
          'account_id': response['info'].get('account_id'),
          'address': response['info'].get('address'),
          'swift': response['info'].get('swift'),
          'ifsc': response['info'].get('ifsc')
        }

        # correspondent info (optional)
        if response['info'].get('correspondent_info'):
            info = response['info']['correspondent_info']
            args['correspondent_swift'] = info.get('swift')
            args['correspondent_bank_name'] = info.get('bank_name')
            args['correspondent_routing_number'] = info.get('routing_num')
            args['correspondent_address'] = info.get('address')
            args['correspondent_swift'] = info.get('swift')

        # balance info (optional)
        if response['info'].get('balance'):
            info = response['info']['balance']
            args['balance'] = info.get('amount')
            args['currency'] = info.get('currency')

        # extra info (optional)
        if response.get('extra'):
            info = response['extra']
            args['supp_id'] = info.get('supp_id')
            args['gateway_restricted'] = info.get('gateway_restricted')

        klass = cls.NODE_TYPES_TO_CLASSES[response['type']]
        return klass(**args)

    @classmethod
    def multiple_from_response(cls, user, response):
        nodes = [cls.from_response(user, node_data)
                 for node_data in response]
        return nodes

    @classmethod
    def by_id(cls, user=None, id=None):
        response = user.client.nodes.get(user.id, id)
        return cls.from_response(user, response)

    @classmethod
    def all(cls, user=None, **kwargs):
        response = user.client.nodes.get(user.id, **kwargs)
        return cls.multiple_from_response(user, response['nodes'])