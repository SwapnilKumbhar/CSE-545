package com.example.cse545project1

import android.content.ContentProvider
import android.content.ContentValues
import android.content.UriMatcher
import android.database.Cursor
import android.database.sqlite.SQLiteQueryBuilder
import android.net.Uri

class ContactsProvider : ContentProvider() {

    companion object {
        private const val AUTHORITY = "com.cse545project.part1.provider.ContactsProvider"
        private const val CONTACTS_TABLE = "contacts"
        val CONTENT_URI : Uri = Uri.parse("content://" + AUTHORITY + "/" +
                CONTACTS_TABLE)
    }

    private val allContacts = 1
    private val singleContact = 2

    private var dbHandler: DBHandler? = null

    private val sUriMatcher = UriMatcher(UriMatcher.NO_MATCH).apply {
        addURI(AUTHORITY, CONTACTS_TABLE, allContacts)
        addURI(AUTHORITY, "$CONTACTS_TABLE/#", singleContact)
    }

    override fun onCreate(): Boolean {
        dbHandler = DBHandler(context, null, null, 1)
        return false
    }

    override fun delete(uri: Uri, selection: String?, selectionArgs: Array<String>?): Int {
        val uriType = sUriMatcher.match(uri)
        val sqlDB = dbHandler!!.writableDatabase

        val rowsDeleted: Int = when (uriType) {
            allContacts -> sqlDB.delete(DBHandler.TABLE_CONTACTS,selection, null)
            singleContact -> sqlDB.delete(DBHandler.TABLE_CONTACTS, selection, null)
            else -> throw IllegalArgumentException("Unknown URI: $uri")
        }
        context!!.contentResolver.notifyChange(uri, null)
        return rowsDeleted
    }

    override fun getType(uri: Uri): String? {
        TODO(
            "Implement this to handle requests for the MIME type of the data" +
                    "at the given URI"
        )
    }

    override fun insert(uri: Uri, values: ContentValues?): Uri? {
        val uriType = sUriMatcher.match(uri)

        val sqlDB = dbHandler!!.writableDatabase

        val id: Long
        when (uriType) {
            allContacts -> id = sqlDB.insert(DBHandler.TABLE_CONTACTS, null, values)
            else -> throw IllegalArgumentException("Unknown URI: $uri")
        }
        context!!.contentResolver.notifyChange(uri, null)
        return Uri.parse("$CONTACTS_TABLE/$id")
    }

    override fun query(
        uri: Uri, projection: Array<String>?, selection: String?,
        selectionArgs: Array<String>?, sortOrder: String?
    ): Cursor? {
        val queryBuilder = SQLiteQueryBuilder()
        queryBuilder.tables = DBHandler.TABLE_CONTACTS

        when (sUriMatcher.match(uri)) {
            singleContact -> queryBuilder.appendWhere(DBHandler.COLUMN_ID + "="
                    + uri.lastPathSegment)
            allContacts -> {
            }
            else -> throw IllegalArgumentException("Unknown URI: $uri")
        }

        val cursor = queryBuilder.query(dbHandler?.readableDatabase,
            projection, selection, selectionArgs, null, null,
            sortOrder)
        cursor.setNotificationUri(context!!.contentResolver,
            uri)
        return cursor
    }

    override fun update(
        uri: Uri, values: ContentValues?, selection: String?,
        selectionArgs: Array<String>?
    ): Int {
        TODO("Implement this to handle requests to update one or more rows.")
    }
}