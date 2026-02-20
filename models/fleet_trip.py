from odoo import models, fields, api

class FleetTrip(models.Model):
    _name = 'fleet.trip'
    _description = 'Vehicle Trip'
    _order = 'start_date desc'

    name = fields.Char(string='Trip Reference', required=True, copy=False, 
                       default=lambda self: self.env['ir.sequence'].next_by_code('fleet.trip') or 'New')
    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', required=True)
    driver_id = fields.Many2one('res.partner', string='Driver', 
                                domain=[('driver', '=', True)])
    start_date = fields.Datetime(string='Start Date', required=True, default=fields.Datetime.now)
    end_date = fields.Datetime(string='End Date')
    start_odometer = fields.Float(string='Start Odometer (km)')
    end_odometer = fields.Float(string='End Odometer (km)')
    distance = fields.Float(string='Distance (km)', compute='_compute_distance', store=True)
    purpose = fields.Text(string='Trip Purpose')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='planned')

    @api.depends('start_odometer', 'end_odometer')
    def _compute_distance(self):
        for trip in self:
            if trip.start_odometer and trip.end_odometer:
                trip.distance = trip.end_odometer - trip.start_odometer
            else:
                trip.distance = 0

    def action_start(self):
        """Start the trip"""
        self.write({'state': 'in_progress', 'start_date': fields.Datetime.now()})

    def action_complete(self):
        """Complete the trip"""
        self.write({'state': 'completed', 'end_date': fields.Datetime.now()})
        # Update vehicle odometer
        if self.end_odometer and self.vehicle_id:
            self.vehicle_id.odometer = self.end_odometer

    def action_cancel(self):
        """Cancel the trip"""
        self.write({'state': 'cancelled'})