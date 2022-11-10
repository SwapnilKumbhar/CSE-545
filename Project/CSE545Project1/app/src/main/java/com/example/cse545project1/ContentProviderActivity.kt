package com.example.cse545project1

import android.net.Uri
import android.os.Bundle
import android.view.View
import android.view.ViewGroup
import android.widget.*
import android.widget.TableRow.LayoutParams
import androidx.appcompat.app.AlertDialog
import androidx.appcompat.app.AppCompatActivity
import com.google.android.material.snackbar.Snackbar


class ContentProviderActivity : AppCompatActivity() {

    private lateinit var tl: TableLayout
    private lateinit var saveContactButton: Button
    private lateinit var clearContactsButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_content_provider)

        val dbHandler = DBHandler(this, null, null, 1)

        tl = findViewById(R.id.contacts_layout)
        saveContactButton = findViewById(R.id.save_contact_button)
        clearContactsButton = findViewById(R.id.clear_contacts_button)

        val allContacts = dbHandler.getAllContacts()

        for (contact in allContacts) {
            addContactRow(contact)
        }

        setSaveContactListener()
        setClearContactsListener()
    }

    /**
     * This method will add a new contact row in the table layout
     */
    private fun addContactRow(contact: Contact) {
        val layoutParams = LayoutParams(LayoutParams.WRAP_CONTENT, LayoutParams.WRAP_CONTENT)
        layoutParams.weight = 1.0F

        val idTextView = TextView(this)
        idTextView.layoutParams = layoutParams
        idTextView.textSize = 16.0F
        idTextView.text = String.format(contact.id.toString())

        val nameTextView = TextView(this)
        nameTextView.layoutParams = layoutParams
        nameTextView.textSize = 16.0F
        nameTextView.text = String.format(contact.name.toString())

        val phoneTextView = TextView(this)
        phoneTextView.layoutParams = layoutParams
        phoneTextView.textSize = 16.0F
        phoneTextView.text = String.format(contact.phone.toString())

        val deleteButtonView = Button(this)
        deleteButtonView.layoutParams = layoutParams
        deleteButtonView.textSize = 10.0F
        deleteButtonView.text = String.format("delete")
        deleteButtonView.setOnClickListener {
            val dbHandler = DBHandler(this, null, null, 1)
            val rowsDeleted: Int = dbHandler.deleteContact(contact)
            val snack = Snackbar.make(it,"Deleted $rowsDeleted contact with name ${contact.name}",Snackbar.LENGTH_LONG)
            snack.show()
            val contactRow: View = findViewById(1000 + contact.id)
            if (contactRow is TableRow) (contactRow as ViewGroup).removeAllViews()
        }

        val tableRow = TableRow(this)
        tableRow.id = 1000 + contact.id
        tableRow.addView(idTextView)
        tableRow.addView(nameTextView)
        tableRow.addView(phoneTextView)
        tableRow.addView(deleteButtonView)

        tl.addView(tableRow)
    }

    /**
     * This method will set a on click listener for saving a new contact
     */
    private fun setSaveContactListener() {

        val dbHandler = DBHandler(this, null, null, 1)

        saveContactButton.setOnClickListener {
            val contactNameView = findViewById<EditText>(R.id.contact_name_edit)
            val phoneNumberView = findViewById<EditText>(R.id.contact_phone_edit)
            val contactName = contactNameView.text.toString()
            val phoneNumber = phoneNumberView.text.toString()

            if("" == contactName.trim() || "" == phoneNumber.trim()) {
                val snack = Snackbar.make(it,"Please enter all details before saving a new contact",Snackbar.LENGTH_SHORT)
                snack.show()
            } else {

                val uri: Uri? = dbHandler.addContact(Contact(contactName, phoneNumber))

                val id: Int = uri!!.lastPathSegment!!.toInt()
                addContactRow(Contact(id, contactName, phoneNumber))

                contactNameView.text.clear()
                phoneNumberView.text.clear()
                contactNameView.clearFocus()
                phoneNumberView.clearFocus()
            }
        }
    }

    /**
     * This method will set a on click listener for clearing all contacts
     */
    private fun setClearContactsListener() {
        val dbHandler = DBHandler(this, null, null, 1)

        clearContactsButton.setOnClickListener {

            val builder = AlertDialog.Builder(this)
            builder.setMessage("Are you sure you want to clear all contacts?")
                .setCancelable(false)
                .setPositiveButton("Yes") { _, _ ->
                    // remove all contacts from the table
                    val rowsDeleted: Int = dbHandler.deleteAllContacts()

                    // display number of deleted contacts
                    val snack = Snackbar.make(it,"$rowsDeleted contacts deleted",Snackbar.LENGTH_LONG)
                    snack.show()

                    // delete all contacts from current view
                    val count: Int = tl.childCount
                    for (i in 0 until count) {
                        // Don't delete table name and table headers
                        if(i < 2) continue
                        val child: View = tl.getChildAt(i)
                        if (child is TableRow) (child as ViewGroup).removeAllViews()
                    }
                }
                .setNegativeButton("No") { dialog, _ ->
                    // Dismiss the dialog
                    dialog.dismiss()
                }
            val alert = builder.create()
            alert.show()
        }

    }

}