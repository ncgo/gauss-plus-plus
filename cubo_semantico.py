# CUBO SEMANTICO
# Diccionario que representa la tabla de consideraciones 
# semánticas (combinaciones factibles y errores de tipo)
#
# GAUSS++
# Nadia Corina Garcia Orozco A01242428
# Noviembre, 2022

cuboSemantico = {
    "+" : {
        "int": {
            "int" : "int",
            "float": "float",
            "bool" : "ERROR",
            "string" : "string"
        }, 
        "float" : {
            "int" : "float",
            "float": "float",
            "bool" : "ERROR",
            "string" : "string"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "string"
        }, 
        "string": {
            "int" : "string",
            "float": "string",
            "bool" : "string",
            "string" : "string"
        }
    },
    "-" : {
        "int": {
            "int" : "int",
            "float": "float",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "float",
            "float": "float",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }
    },
    "*" : {
        "int": {
            "int" : "int",
            "float": "float",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "float",
            "float": "float",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }
    },
    "/" : {
        "int": {
            "int" : "float",
            "float": "float",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "float",
            "float": "float",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }
    },
     "=" : {
        "int": {
            "int" : "int",
            "float": "float",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "float",
            "float": "float",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "bool",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "string"
        }
    },
    "==" : {
        "int": {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "bool",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "bool"
        }
    },
    "!=" : {
        "int": {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "bool",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "bool"
        }
    },
    ">" : {
        "int": {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }
    },
    "<" : {
        "int": {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }
    },
    ">=" : {
        "int": {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }
    },
    "<=" : {
        "int": {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "bool",
            "float": "bool",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }
    },
    "and" : {
        "int": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "bool",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }
    },
    "or" : {
        "int": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }, 
        "float" : {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        },
        "bool": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "bool",
            "string" : "ERROR"
        }, 
        "string": {
            "int" : "ERROR",
            "float": "ERROR",
            "bool" : "ERROR",
            "string" : "ERROR"
        }
    }
}