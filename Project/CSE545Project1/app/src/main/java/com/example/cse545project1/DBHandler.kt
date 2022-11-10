package com.example.cse545project1

import android.content.ContentResolver
import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper
import android.net.Uri

class DBHandler(
    context: Context?, name: String?,
    factory: SQLiteDatabase.CursorFactory?, version: Int
) :
    SQLiteOpenHelper(
        context, DATABASE_NAME,
        factory, DATABASE_VERSION
    ) {

    private val contentResolver: ContentResolver? = context!!.contentResolver

    companion object {

        private const val DATABASE_VERSION = 1
        private const val DATABASE_NAME = "contactDB.db"
        const val TABLE_CONTACTS = "contacts"
        const val TABLE_SQLITE_SEQUENCE = "sqlite_sequence"

        const val COLUMN_ID = "_id"
        const val COLUMN_NAME = "name"
        const val COLUMN_PHONE = "phone"
    }

    override fun onCreate(db: SQLiteDatabase) {
        val createContactsTable = ("CREATE TABLE " +
                TABLE_CONTACTS + "("
                + COLUMN_ID + " INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL," +
                COLUMN_NAME
                + " TEXT," + COLUMN_PHONE + " TEXT" + ")")
        db.execSQL(createContactsTable)
    }

    override fun onUpgrade(
        db: SQLiteDatabase, oldVersion: Int,
        newVersion: Int
    ) {
        db.execSQL("DROP TABLE IF EXISTS $TABLE_CONTACTS")
        onCreate(db)
    }

    fun addContact(contact: Contact): Uri? {
        val values = ContentValues()
        values.put(COLUMN_NAME, contact.name)
        values.put(COLUMN_PHONE, contact.phone)

        return contentResolver!!.insert(ContactsProvider.CONTENT_URI, values)
    }

    fun getAllContacts(): ArrayList<Contact> {
        val projection = arrayOf(COLUMN_ID, COLUMN_NAME, COLUMN_PHONE)

        val allContacts = ArrayList<Contact>()

        val cursor = contentResolver!!.query(ContactsProvider.CONTENT_URI,
            projection, null, null, null)

        if (cursor!!.moveToFirst()) {
            cursor.moveToFirst()
            do {
                var contact: Contact?
                val id = Integer.parseInt(cursor.getString(0))
                val name = cursor.getString(1)
                val phone = cursor.getString(2)
                contact = Contact(id, name, phone)
                allContacts.add(contact)
            } while (cursor.moveToNext())
        }

        cursor.close()
        return allContacts
    }

    fun deleteContact(contact: Contact): Int {
        val selection = "_id = \"${contact.id}\""

        return contentResolver!!.delete(
            ContactsProvider.CONTENT_URI,
            selection, null
        )
    }

    fun deleteAllContacts(): Int {

        val selection = "1"

        val db = this.writableDatabase
        db.execSQL("DELETE from $TABLE_SQLITE_SEQUENCE where name=\'$TABLE_CONTACTS\'")

        return contentResolver!!.delete(
            ContactsProvider.CONTENT_URI,
            selection, null
        )
    }
}