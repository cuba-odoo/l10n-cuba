from odoo import api, SUPERUSER_ID


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})

    env.cr.execute("""
        UPDATE res_partner
        SET municipality_id = NULL
        WHERE municipality_id IS NOT NULL
          AND (
              state_id IS NULL
              OR municipality_id NOT IN (
                  SELECT id
                  FROM res_municipality
                  WHERE state_id = res_partner.state_id
              )
          )
    """)
