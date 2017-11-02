module.exports = {
    "name": "input-schema",
    "type": "object",
    "properties": {
        "inputs":{
          "type": "array"
        },
        "job": {
            "type": "object",
            "properties": {
                "type": {
                    "type": "string",
                    "required": true,
                    "description": "the job type"
                }
            }
        },
        "setting": {
            "type": "object",
            "properties": {
                "prefix": {
                    "type": "string",
                    "default": "jobs",
                    "description": "prefix for all queue keys"
                },
                "redis": {
                    "type": "object",
                    "properties": {
                        "host": {
                            "type": "string",
                            "default": "localhost"
                        },
                        "port": {
                            "type": ["integer", "string"],
                            "default": 6379
                        }
                    }
                }
            }
        }
    }
}

const initMessage = {
    command: "initialize",
    data:{
        input:[
            "input1",
            "input2",
            {foo:"bar"}
        ]

    }
}

const initMessage = {
    command: "initialize",
    data:{
        input:[
            "input1",
            "input2",
            {foo:"bar"}
        ]

    }
}
const resultMessage={
    command: "done",
    data:{
        result:[
            "output 1",
            "output 2"
        ]
    }
}
const progressMessage = {
    command: "progress",
    data:{
        progress: 50,
        details: "Optional extra details"
    }
}
const input = {
    input:[
        "input1",
        "input2",
        {foo:"bar"}
    ]
}

const outputOK = {
    resultCode: "Ok",
    output: [
        "output 1",
        "output 2"
    ]
}

const outputError = {
    resultCode: "Error",
    error: "Error description"
}

const progress = {
    progress: 10, // progress percentage
    timestamp: xxx // timestamp in unix epoch. Used to detect hung progress
}

module.exports={
    outgoing:{
        pong:'pong',
        initialized:'initialized',
        started:'started',
        stopped:'stopped',
        progress:'progress',
        done:'done'

    },
    incomming:{
        ping:'ping',
        initialize:'initialize',
        start:'start',
        cleanup:'cleanup',
        stop:'stop'

    }
}

const message = {
    command: "command",
    data:{

    }
}