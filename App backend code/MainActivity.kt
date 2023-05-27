package com.example.movesmart

import android.content.Intent
import android.os.Bundle
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        val clicksummary = findViewById<ImageView>(R.id.summary_button1)
        clicksummary.setOnClickListener {
            val intent = Intent(this,MainActivity2::class.java)
            startActivity(intent)
            clicksummary.setColorFilter(ContextCompat.getColor(this, R.color.button_colourchange))
        }

        val clickmovement = findViewById<ImageView>(R.id.movement_button1)
        clickmovement.setOnClickListener {
            val intent = Intent(this,MainActivity3::class.java)
            startActivity(intent)
            clickmovement.setColorFilter(ContextCompat.getColor(this, R.color.button_colourchange))
        }

    }
}