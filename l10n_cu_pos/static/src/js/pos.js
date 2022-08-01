odoo.define('l10n_cu_pos.pos', function (require) {
"use strict";
    const { useState } = owl;
    const models = require('point_of_sale.models');
    models.load_fields('res.partner', ['is_company', 'cnae_primary']);

    models.load_models({
        model:  'res.cnae',
        label: 'CNAE',
        fields: ['id', 'code', 'name'],
        loaded: function(self, cnaes){
            self.cnaes = cnaes;
        },
    });

    const ClientDetailsEdit = require('point_of_sale.ClientDetailsEdit');
    const Registries = require("point_of_sale.Registries");

    const ClientDetailsEditInherit = (ClientDetailsEdit) =>
        class extends ClientDetailsEdit {
            constructor() {
                super(...arguments);
                this.state = useState({
                    'is_company': this.props.partner.is_company,
                });
            }
            saveChanges() {
                if (this.state.is_company) {
                    this.changes.is_company = true;
                    this.changes.cnae_primary = $("#cnae_id").val();
                } else {
                    this.changes.is_company = false;
                }
                super.saveChanges();
            }
        };

    Registries.Component.extend(ClientDetailsEdit, ClientDetailsEditInherit);

    return ClientDetailsEdit;
});