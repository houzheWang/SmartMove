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

class Lift_mode : AppCompatActivity() {
    private val LOG_TAG = "Lift_mode"
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_lift_mode)

        val goback = findViewById<ImageView>(R.id.lift_goback)
        goback.setOnClickListener {
            val intent = Intent(this,MainActivity3::class.java)
            startActivity(intent)
            val write = FirebaseDatabase.getInstance().getReference("level1")
            write.setValue(0)
        }

        val clickstop2 = findViewById<ImageView>(R.id.stoplift)
        clickstop2.setOnClickListener {
            val write = FirebaseDatabase.getInstance().getReference("level1")
            write.setValue(3)
        }
    }

    override fun onStart() {
        super.onStart()
        val lift_ref = FirebaseDatabase.getInstance().getReference("postlist2")
        lift_ref.addValueEventListener(listener2)
    }
    override fun onStop() {
        val lift_ref = FirebaseDatabase.getInstance().getReference("postlist2")
        lift_ref.removeEventListener(listener2)
        super.onStop()
    }

    private val listener2 = object : ValueEventListener {

        override fun onDataChange(data: DataSnapshot) {
            data.children.forEach{

                val left_percent2 = it.child("Left").value.toString()
                val force_left2 = findViewById<TextView>(R.id.readleft2)
                force_left2.text = left_percent2

                val right_percent2 = it.child("Right").value.toString()
                val force_right2 = findViewById<TextView>(R.id.readright2)
                force_right2.text = right_percent2

                val left_force2 = it.child("Left").getValue(Int::class.java)
                if(left_force2 != null){
                    val leftfoot_shape2 = findViewById<ImageView>(R.id.left_shape2)
                    val parameters2 = leftfoot_shape2.layoutParams
                    val lf2 = left_force2 * 7
                    parameters2.height = lf2
                    parameters2.width = lf2
                    leftfoot_shape2.layoutParams = parameters2
                }

                val right_force2 = it.child("Right").getValue(Int::class.java)
                if(right_force2 != null){
                    val rightfoot_shape2 = findViewById<ImageView>(R.id.right_shape2)
                    val parameters2 = rightfoot_shape2.layoutParams
                    val rf2 = right_force2 * 7
                    parameters2.height = rf2
                    parameters2.width = rf2
                    rightfoot_shape2.layoutParams = parameters2
                }
            }
        }
        override fun onCancelled(databaseError: DatabaseError) {
            Log.e(LOG_TAG, "Database error", databaseError.toException())
        }
    }
}