resources = [

    {
        "path": "/dashboard/admin/",
                "method": "GET",
                "icono": "pi pi-home",
                "id_padre": 0,
                "link": "/dashboard/admin/",
                "titulo": "Admin",
                "items": [
                    {
                        "path": "/dashboard/admin/roles-recursos/",
                        "method": "GET",
                        "icono": "pi pi-home",
                        "link": "/dashboard/admin/roles-recursos/",
                        "titulo": "Roles Y Recursos",
                        "items": [
                            {
                                "path": "/dashboard/admin/roles-recursos/ver-crear/",
                                "method": "POST",
                                "icono": "icon",
                                "link": "/dashboard/admin/roles-recursos/ver-editar/",
                                "titulo": "Ver Editar"
                            },
                            {
                                "path": "/dashboard/admin/roles-recursos/ver/",
                                "method": "GET",
                                "icono": "icon",
                                "link": "/dashboard/admin/roles-recursos/crear/",
                                "titulo": "Crear"
                            }
                        ]
                    },
                    {
                        "path": "/dashboard/admin/roles/",
                        "method": "GET",
                        "icono": "pi pi-user-minus",
                        "link": "/dashboard/admin/roles/",
                        "titulo": "Roles",
                        "items": [
                            {
                                "path": "/dashboard/admin/roles/ver/",
                                "method": "POST",
                                "icono": "icon",
                                "link": "/dashboard/admin/roles/ver/",
                                "titulo": "Ver"
                            }
                        ]
                    },
                ]
    },
    {
        "path": "/dashboard/persona/",
                "method": "GET",
                "icono": "pi pi-user",
                "id_padre": 0,
                "link": "/dashboard/persona/",
                "titulo": "Persona",
                "items": [
                    {
                        "path": "/dashboard/persona/datos-personales/",
                        "method": "GET",
                        "icono": "icon",
                        "link": "/dashboard/persona/datos-personales/",
                        "titulo": "Datos Personales",
                        "items": [
                            {
                                "path": "/dashboard/persona/datos-personales/ver/",
                                "method": "GET",
                                "icono": "icon",
                                "link": "/dashboard/persona/datos-personales/ver/",
                                "titulo": "Ver"
                            }
                        ]
                    }
                ]
    }

]
