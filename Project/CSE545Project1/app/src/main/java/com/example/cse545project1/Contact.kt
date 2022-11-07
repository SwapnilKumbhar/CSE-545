package com.example.cse545project1

class Contact {

    var id: Int = 0
    var name: String? = null
    var phone: String? = null

    constructor(id: Int, name: String, phone: String) {
        this.id = id
        this.name = name
        this.phone = phone
    }

    constructor(name: String, phone: String) {
        this.name = name
        this.phone = phone
    }

}