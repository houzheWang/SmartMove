package com.example.movesmart

import android.content.Intent
import android.os.Bundle
import android.widget.Button
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.google.firebase.database.FirebaseDatabase

class MainActivity3 : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main3)

        val clicksummary3 = findViewById<ImageView>(R.id.summary_button3)
        clicksummary3.setOnClickListener {
            val intent = Intent(this,MainActivity2::class.java)
            startActivity(intent)
            clicksummary3.setColorFilter(ContextCompat.getColor(this, R.color.button_colourchange))
        }
        val clickhome3 = findViewById<ImageView>(R.id.home_button3)
        clickhome3.setOnClickListener {
            val intent = Intent(this,MainActivity::class.java)
            startActivity(intent)
            clickhome3.setColorFilter(ContextCompat.getColor(this, R.color.button_colourchange))
        }
        val clickrunmode = findViewById<Button>(R.id.run_button)
        clickrunmode.setOnClickListener {
            val intent = Intent(this,running_mode::class.java)
            startActivity(intent)
            val write = FirebaseDatabase.getInstance().getReference("level1")
            write.setValue(1)
        }
        val clickliftmode = findViewById<Button>(R.id.lift_button)
        clickliftmode.setOnClickListener {
            val intent = Intent(this,Lift_mode::class.java)
            startActivity(intent)
            val write = FirebaseDatabase.getInstance().getReference("level1")
            write.setValue(2)
        }
    }
}


