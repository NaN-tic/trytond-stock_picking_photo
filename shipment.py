#This file is part stock_picking_photo module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.wizard import StateTransition, Button
from trytond.pool import Pool, PoolMeta

__all__ = ['ShipmentOutPickingResult', 'ShipmentOutPacked']
__metaclass__ = PoolMeta


class ShipmentOutPickingResult:
    __name__ = 'stock.shipment.out.picking.result'
    photo = fields.Binary('Photo',
        help='Select a file to attach to the Shipment Out')


class ShipmentOutPacked:
    __name__ = 'stock.shipment.out.packed'
    photo = StateTransition()

    @classmethod
    def __setup__(cls):
        super(ShipmentOutPacked, cls).__setup__()
        # add new button: Save Photo
        cls.result.buttons.insert(0, 
            Button('Save Photo', 'photo', 'tryton-go-next', True))

    def transition_photo(self):
        pool = Pool()
        Attachment = pool.get('ir.attachment')

        shipment = self.result.shipment
        photo = self.result.photo

        if photo:
            attach = Attachment(
                name='shipment-out-%s' % shipment.rec_name,
                type='data',
                data=photo,
                resource=str(shipment))
            attach.save()
        return 'start'
