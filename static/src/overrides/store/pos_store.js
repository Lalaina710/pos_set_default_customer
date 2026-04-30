/** @odoo-module **/

import { PosStore } from "@point_of_sale/app/store/pos_store";
import { patch } from "@web/core/utils/patch";
import { _t } from "@web/core/l10n/translation";

patch(PosStore.prototype, {
    async selectPartner() {
        const isManager = this.user && this.user._role === "manager";
        if (!isManager && this.config && this.config.default_partner_id) {
            this.notification.add(
                _t("Changement de client non autorisé. Contacter un manager."),
                4000
            );
            return this.get_order() ? this.get_order().get_partner() : false;
        }
        return super.selectPartner(...arguments);
    },
});
