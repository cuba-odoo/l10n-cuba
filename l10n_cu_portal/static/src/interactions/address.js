/** @odoo-module **/

import { CustomerAddress } from "@portal/interactions/address";
import { rpc } from "@web/core/network/rpc";
import { patch } from "@web/core/utils/patch";

patch(CustomerAddress.prototype, {
    setup() {
        super.setup();
        this._updateCubanCityFields();
    },

    async onChangeCountry() {
        const countryId = this.addressForm.country_id.value;
        const data = await this.waitFor(super.onChangeCountry(...arguments));
        if (this.addressForm.country_id.value === countryId && this.addressForm.municipality_id) {
            this._updateCubanCityFields();
            await this.waitFor(this._updateMunicipalities());
        }
        return data;
    },

    async onChangeState() {
        const data = await this.waitFor(super.onChangeState(...arguments));
        await this.waitFor(this._updateMunicipalities());
        return data;
    },

    _updateCubanCityFields() {
        if (
            this.addressForm.municipality_id &&
            this._getSelectedCountryCode() === "CU" &&
            this.requiredFields.includes("municipality_id")
        ) {
            this._hideInput("city");
            this._hideInput("city_id");
        }
    },

    async _updateMunicipalities() {
        const municipality = this.addressForm.municipality_id;
        if (!municipality) {
            return;
        }
        const stateId = this.addressForm.state_id.value;
        const selectedId = municipality.value;
        this._setFieldChoices("municipality_id", []);
        if (this._getSelectedCountryCode() !== "CU" || !stateId) {
            return;
        }

        const { municipalities } = await this.waitFor(
            rpc(`/shop/l10n_cu/state_infos/${stateId}`, {})
        );
        if (this._getSelectedCountryCode() !== "CU" || this.addressForm.state_id.value !== stateId) {
            return;
        }
        this._setFieldChoices(
            "municipality_id",
            municipalities.map(([id, name, code]) => ({ id, name, code }))
        );
        if (municipalities.some(([id]) => String(id) === selectedId)) {
            municipality.value = selectedId;
        }
    },
});
