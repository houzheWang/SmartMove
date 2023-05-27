package com.example.movesmart

import android.content.Intent
import android.os.Bundle
import android.util.Log
import android.widget.ImageView
import android.widget.TextView
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener

class running_mode : AppCompatActivity() {
    private val LOG_TAG = "running_mode"

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_running_mode)

        val goback = findViewById<ImageView>(R.id.run_goback)
        goback.setOnClickListener {
            val intent = Intent(this,MainActivity3::class.java)
            startActivity(intent)
            val write = FirebaseDatabase.getInstance().getReference("level1")
            write.setValue(0)
        }
        val clickpuase = findViewById<ImageView>(R.id.pause)
        clickpuase.setOnClickListener {
            val write = FirebaseDatabase.getInstance().getReference("level1")
            write.setValue(4)
        }
        val clickresume = findViewById<ImageView>(R.id.resume)
        clickresume.setOnClickListener {
            val write = FirebaseDatabase.getInstance().getReference("level1")
            write.setValue(5)
        }
        val clickstop = findViewById<ImageView>(R.id.stop)
        clickstop.setOnClickListener {
            val write = FirebaseDatabase.getInstance().getReference("level1")
            write.setValue(3)
        }
    }
    override fun onStart() {
        super.onStart()
        val ref = FirebaseDatabase.getInstance().getReference("postlist")
        ref.addValueEventListener(listener1)
    }
    override fun onStop() {
        val ref = FirebaseDatabase.getInstance().getReference("postlist")
        ref.removeEventListener(listener1)
        super.onStop()
    }

    private val listener1 = object : ValueEventListener {
        override fun onDataChange(data: DataSnapshot) {
            data.children.forEach{

                val left_percent = it.child("Left_Percentage").value.toString()
                val force_left = findViewById<TextView>(R.id.readleft)
                force_left.text = left_percent

                val right_percent = it.child("Right_Percentage").value.toString()
                val force_right = findViewById<TextView>(R.id.readright)
                force_right.text = right_percent


                val F_Advice = it.child("Force_Advice").value
                val f_d = findViewById<TextView>(R.id.force_advice)
                f_d.text = F_Advice.toString()

                val P_Advice = it.child("Pace_Advice").value
                val p_d = findViewById<TextView>(R.id.pace_advice)
                p_d.text = P_Advice.toString()

                val Temp = it.child("temperature").value
                val temp_shown = findViewById<TextView>(R.id.temp)
                temp_shown.text = Temp.toString()


                val left_force = it.child("Left_Percentage").getValue(Int::class.java)
                if(left_force != null){
                    val leftfoot_shape = findViewById<ImageView>(R.id.left_shape)
                    val parameters = leftfoot_shape.layoutParams
                    val lf = left_force * 7
                    parameters.height = lf
                    parameters.width = lf
                    leftfoot_shape.layoutParams = parameters
                }

                val right_force = it.child("Right_Percentage").getValue(Int::class.java)
                if(right_force != null){
                    val rightfoot_shape = findViewById<ImageView>(R.id.right_shape)
                    val parameters = rightfoot_shape.layoutParams
                    val rf = right_force * 7
                    parameters.height = rf
                    parameters.width = rf
                    rightfoot_shape.layoutParams = parameters
                }
            }
        }
        override fun onCancelled(databaseError: DatabaseError) {
            Log.e(LOG_TAG, "Database error", databaseError.toException())
        }
    }
}