import { generateApplicationSchema } from "./application_base_schema.js";
import { generateVendorSchema } from "./vendor_base_schema.js";
import { versionBaseSchema } from "./version_base_schema.js";
import { roleSchema } from "./role_schema.js";
import { systemTypeSchema } from "./system_type_schema.js";

export const vendorSchema = generateVendorSchema({
    applications: {
        type: "array",
        items: generateApplicationSchema({
            versions: {
                type: "array",
                items: versionBaseSchema
            },
            roles: {
                type: "array",
                items: roleSchema
            },
            systemTypes: {
                type: "array",
                items: systemTypeSchema
            }
        }),
    }
})
