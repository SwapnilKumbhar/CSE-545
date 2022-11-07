package com.example.cse545project1

import android.content.Intent
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.widget.Button
import android.view.View

class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val contentProviderButton = findViewById<Button>(R.id.content_provider_button)
        contentProviderButton.setOnClickListener {
            val intent = Intent(this, ContentProviderActivity::class.java)
            startActivity(intent)
        }
    }

    // Callbacks
    fun onServiceClick(v: View) {
        // Starts the service activity
        startActivity(Intent(this, ServiceActivity::class.java))
    }

}