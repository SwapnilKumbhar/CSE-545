package com.example.cse545project1

import android.content.Intent
import android.os.Bundle
import android.view.View
import android.widget.Button
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import java.text.SimpleDateFormat
import java.util.*

class MainActivity : AppCompatActivity() {
    private val _dateFormatter = SimpleDateFormat("HH:mm")

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val contentProviderButton = findViewById<Button>(R.id.content_provider_button)
        contentProviderButton.setOnClickListener {
            val intent = Intent(this, ContentProviderActivity::class.java)
            startActivity(intent)
        }

        // Update text view with current time
        val currTimeTv = findViewById<TextView>(R.id.main_curr_time)
        currTimeTv.text = _dateFormatter.format(Date())
    }

    // Callbacks
    fun onServiceClick(v: View) {
        // Starts the service activity
        startActivity(Intent(this, ServiceActivity::class.java))
    }

    fun onBroadcastClick(v: View) {
        startActivity(Intent(this, BroadcastActivity::class.java))
    }

}