/** @odoo-module **/

import { CustomerAddress } from "@portal/interactions/address";
import { rpc } from "@web/core/network/rpc";
import { patch } from "@web/core/utils/patch";

patch(CustomerAddress.prototype, {
    setup() {
        super.setup();

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

    async onChangeState() {
        await this.waitFor(super.onChangeState());
        let selectedCountry = this.elementCountry.value ?
            this.elementCountry.selectedOptions[0].getAttribute('code') : '';
        if (selectedCountry === "CU") {
            const stateId = this.elementState.value;
            let choices = [];
            if (stateId)  {
                const data = await this.waitFor(rpc(`/shop/l10n_cu/state_infos/${stateId}`, {}));
                choices = data.municipalities;
            }
            this._changeOption(this.elementMunicipalities, choices);
        }
    },


    async _onChangeCountry(init=false) {
        await this.waitFor(super._onChangeCountry(...arguments));
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
