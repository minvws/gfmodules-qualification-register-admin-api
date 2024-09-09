export const validationItemSchema = {
    type: "object",
    properties: {
        loc: {
            type: "array",
        },
        msg: {
            type: "string",
        },
        type: {
            type: "string",
        },
    },
    required: [
        "loc",
        "msg",
        "type"
    ]
}

export const validationErrorResponseSchema = {
    type: "object",
    properties: {
        detail: {
            type: "array",
            items: validationItemSchema
        }
    },
    required: [
        "detail"
    ]
}

export const notFoundResponseSchema = {
    type: "object",
    properties: {
        detail: {
            type: "string",
        },
    },
    required: [
        "detail"
    ]
}