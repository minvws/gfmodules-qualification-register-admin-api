export const healthResponseSchema = {
    type: "object",
    properties: {
        status: {
            enum: ["ok"]
        },
        components: {
            type: "object",
            properties: {
                database: {
                    enum: ["ok"]
                }
            }
        },
    },
    required: [
        "status",
        "components",
    ]
}