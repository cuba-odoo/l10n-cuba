/** @odoo-module **/
import { WebsiteSale } from "@website_sale/js/website_sale";

WebsiteSale.include({
    start: function () {
        this.elementMunicipalities = document.querySelector("select[name='res_municipality_id']");
        this.municipalityBlock = document.querySelector(".div_municipality");
        this.elementState = document.querySelector("select[name='state_id']");
        this.elemenCountry = document.querySelector("select[name='country_id']");
        return this._super.apply(this, arguments);
    },
    _onChangeState: function (ev) {
        return this._super.apply(this, arguments).then(() => {
            let selectedCountry = this.elemenCountry.options[this.elemenCountry.selectedIndex].getAttribute("code");
            if (selectedCountry === "CU") {

                if (!this.$('.checkout_autoformat').length) {
                    return;
                }

                if (this.elementState.value === "" && this.elemenCountry.value !== '') {
                    this.elementState.options[1].selected = true;
                }
                const state = this.elementState.value;
                return this.rpc(`/shop/l10n_cu/state_infos/${state}`, {
                    mode: $("#country_id").attr('mode'),
                }).then((data) => {
                    // populate municipalities and display

                    var selectMunicipalities = $("select[name='res_municipality_id']");
                    // dont reload municipality at first loading (done in qweb)
                    if (selectMunicipalities.data('init') === 0 || selectMunicipalities.find('option').length === 1) {
                        if (data.municipalities.length || data.municipality_required) {
                            selectMunicipalities.html('');
                            data.municipalities.forEach((x) => {
                                var opt = $('<option>').text(x[1])
                                    .attr('value', x[0])
                                    .attr('data-code', x[2]);
                                selectMunicipalities.append(opt);
                            });
                            selectMunicipalities.parent('div').show();
                        } else {
                            selectMunicipalities.val('').parent('div').hide();
                        }
                        selectMunicipalities.data('init', 0);
                    } else {
                        selectMunicipalities.data('init', 0);
                    }
                });
            }
        });
    },
    _onChangeCountry: function (ev) {
        return this._super.apply(this, arguments).then(() => {
            let selectedCountry = ev.currentTarget.options[ev.currentTarget.selectedIndex].getAttribute("code");
            if (selectedCountry === "CU") {
                return this._onChangeState();
            } else {
                this.municipalityBlock.querySelectorAll("input").forEach((input) => {
                    input.value = "";
                });
                this.municipalityBlock.classList.remove("d-none");
                this.elementMunicipalities.value = "";
                this.elementMunicipalities.parentElement.style.display = "none";
            }
        });
    },
});
