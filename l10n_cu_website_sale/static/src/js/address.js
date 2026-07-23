/** @odoo-module **/

import websiteSaleAddress from "@website_sale/js/address";
import { rpc } from "@web/core/network/rpc";

websiteSaleAddress.include({
    start: function () {
        this._super.apply(this, arguments);

        this.elementCountry = this.addressForm.country_id;
        this.elementState = this.addressForm.state_id;
        this.elementMunicipalities = this.addressForm.municipality_id;

    },

    _changeOption(selectElement, choices) {
        // empty existing options, only keep the placeholder.
        selectElement.options.length = 1;
        if (choices.length) {
            choices.forEach((item) => {
                let option = new Option(item[1], item[0]);
                option.setAttribute('data-code', item[2]);
                selectElement.appendChild(option);
            });
        }
    },

    async _onChangeState() {
        await this._super(...arguments);
        let selectedCountry = this.elementCountry.value ?
            this.elementCountry.selectedOptions[0].getAttribute('code') : '';
        if (selectedCountry === "CU") {
            const stateId = this.elementState.value;
            let choices = [];
            if (stateId)  {
                const data = await rpc(`/shop/l10n_cu/state_infos/${stateId}`, {});
                choices = data.municipalities;
            }
            this._changeOption(this.elementMunicipalities, choices);
        }
    },


    async _changeCountry(init=false) {
        await this._super(...arguments);
        let selectedCountry = this.elementCountry.value ?
            this.elementCountry.selectedOptions[0].getAttribute('code') : '';
        if (selectedCountry === 'CU') {
            this._showInput('municipality_id');
        } else {
            // empty existing options, only keep the placeholder.
            this.elementMunicipalities.options.length = 1;
            this._hideInput('municipality_id');
        }

    },
});
