#This file is part stock_picking_photo module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import ModelView, fields
from trytond.wizard import StateTransition, StateView, Button
from trytond.pool import Pool, PoolMeta
import hashlib

__all__ = ['ShipmentOutPickingPhoto', 'ShipmentOutPacked']


class ShipmentOutPickingPhoto(ModelView):
    'Shipment Out Picking Photo'
    __name__ = 'stock.shipment.out.picking.photo'
    shipment = fields.Many2One('stock.shipment.out', 'Shipment', readonly=True)
    attach = fields.Binary('Attach',
        help='Select a file to attach to the Shipment Out')


class ShipmentOutPacked:
    __metaclass__ = PoolMeta
    __name__ = 'stock.shipment.out.packed'
    photo = StateTransition()
    photo_ask = StateView('stock.shipment.out.picking.photo',
        'stock_picking_photo.stock_shipment_out_picking_photo', [
            Button('Cancel', 'end', 'tryton-cancel'),
            Button('New picking', 'picking', 'tryton-go-next'),
            Button('Save and New', 'photo', 'tryton-go-next', True),
            ])

    @classmethod
    def __setup__(cls):
        super(ShipmentOutPacked, cls).__setup__()
        # add new button: Add Photo
        cls.result.buttons.insert(0, 
            Button('Add Photo', 'photo_ask', 'tryton-go-next', True))

    def default_photo_ask(self, fields):
        return {
            'shipment': self.result.shipment.id,
            }

    def transition_photo(self):
        pool = Pool()
        Attachment = pool.get('ir.attachment')

        shipment = self.photo_ask.shipment
        attach = self.photo_ask.attach
        if attach:
            hashname = hashlib.md5(attach).hexdigest()
            attachment = Attachment(
                name='%s-%s' % (shipment.rec_name, hashname),
                type='data',
                data=attach,
                resource=str(shipment))
            attachment.save()
        return 'photo_ask'
