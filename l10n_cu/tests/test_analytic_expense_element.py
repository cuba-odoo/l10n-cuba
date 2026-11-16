# -*- coding: utf-8 -*-
from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestAnalyticExpenseElement(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Account = cls.env['account.analytic.account']
        cls.Element = cls.env['expense.element']
        cls.plan = cls.env['account.analytic.plan'].create({'name': 'Test plan'})
        cls.element = cls.Element.create({'name': 'Materials', 'code': '100'})
        cls.regular = cls.Account.create({'name': 'Regular', 'plan_id': cls.plan.id})

    def test_regular_accounts_not_archived(self):
        """Creating or writing regular accounts must never archive other accounts (issue #37)."""
        new = self.Account.create({'name': 'New project', 'plan_id': self.plan.id})
        self.assertTrue(new.active)
        self.assertTrue(self.regular.active)
        self.regular.write({'name': 'Regular renamed'})
        self.assertTrue(self.regular.active)

    def test_regular_account_can_be_unarchived(self):
        self.regular.action_archive()
        self.assertFalse(self.regular.active)
        self.regular.action_unarchive()
        self.assertTrue(self.regular.active)

    def test_combinations_lifecycle(self):
        container = self.Account.create({
            'name': 'Container', 'code': 'C1', 'plan_id': self.plan.id, 'element_detailed': True,
        })
        combined = self.Account.search([('parent_id', '=', container.id), ('element_id', '=', self.element.id)])
        self.assertEqual(len(combined), 1)
        self.assertEqual(combined.code, 'C1.100')
        # The element stops being a leaf: its combination is archived, a new one is created for the child
        child = self.Element.create({'name': 'Steel', 'code': '101', 'parent_id': self.element.id})
        self.assertFalse(combined.active)
        child_combined = self.Account.search([('parent_id', '=', container.id), ('element_id', '=', child.id)])
        self.assertEqual(len(child_combined), 1)
        self.assertTrue(self.regular.active)
        self.assertTrue(container.active)
        # The element becomes a leaf again: its combination is unarchived
        child.unlink()
        self.env['expense.element']._create_aa_childs()
        self.assertTrue(combined.active)

    def test_container_cannot_have_element(self):
        with self.assertRaises(ValidationError):
            self.Account.create({
                'name': 'Bad', 'plan_id': self.plan.id,
                'element_detailed': True, 'element_id': self.element.id,
            })
