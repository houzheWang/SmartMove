package com.example.movesmart

import android.content.Intent
import android.graphics.Color
import android.os.Bundle
import android.util.Log
import android.widget.Button
import android.widget.ImageView
import androidx.appcompat.app.AppCompatActivity
import androidx.core.content.ContextCompat
import com.github.mikephil.charting.animation.Easing
import com.github.mikephil.charting.data.Entry
import com.github.mikephil.charting.data.LineData
import com.github.mikephil.charting.data.LineDataSet
import com.google.firebase.database.DataSnapshot
import com.google.firebase.database.DatabaseError
import com.google.firebase.database.FirebaseDatabase
import com.google.firebase.database.ValueEventListener

class MainActivity2 : AppCompatActivity() {
    private val LOG_TAG = "MainActivity2"
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main2)

        val clickmovement2 = findViewById<ImageView>(R.id.movement_button2)
        clickmovement2.setOnClickListener {
            val intent = Intent(this,MainActivity3::class.java)
            startActivity(intent)
            clickmovement2.setColorFilter(ContextCompat.getColor(this, R.color.button_colourchange))
        }

        val clickhome2 = findViewById<ImageView>(R.id.home_button2)
        clickhome2.setOnClickListener {
            val intent = Intent(this,MainActivity::class.java)
            startActivity(intent)
            clickhome2.setColorFilter(ContextCompat.getColor(this, R.color.button_colourchange))
        }

        //generating running history
        val run_his = findViewById<Button>(R.id.run_plot)
        run_his.setOnClickListener {


            val ref = FirebaseDatabase.getInstance().getReference("postlist")

            ref.addListenerForSingleValueEvent(object : ValueEventListener {
                override fun onDataChange(data: DataSnapshot) {
                    val entries = ArrayList<Entry>()
                    val entries_l = ArrayList<Entry>()
                    for (childSnapshot in data.children) {
                        val xValue = childSnapshot.child("time").getValue(Float::class.java)
                        val yValue = childSnapshot.child("Right_Percentage").getValue(Float::class.java)
                        if(xValue != null && yValue != null){
                        entries.add(Entry(xValue, yValue))
                        }

                        val xValue_l = childSnapshot.child("time").getValue(Float::class.java)
                        val yValue_l = childSnapshot.child("Left_Percentage").getValue(Float::class.java)
                        if(xValue_l != null && yValue_l != null){
                            entries_l.add(Entry(xValue_l, yValue_l))
                        }
                    }
                    val vl = LineDataSet(entries, "Right foot force history")
                    val vl_l = LineDataSet(entries_l,"Left foot force history")

                    vl.setDrawValues(false)
                    vl.setDrawFilled(true)
                    vl.color = Color.BLUE
                    vl.lineWidth = 3f
                    vl.fillColor = R.color.gray
                    vl.fillAlpha = R.color.lightblue

                    vl_l.setDrawValues(false)
                    vl_l.setDrawFilled(true)
                    vl_l.color = Color.RED
                    vl_l.lineWidth = 3f
                    vl_l.fillColor = R.color.gray
                    vl_l.fillAlpha = R.color.lightblue

                    val lineChart = findViewById<com.github.mikephil.charting.charts.LineChart>(R.id.force_lineChart)
                    lineChart.xAxis.labelRotationAngle = 0f

                    lineChart.axisRight.isEnabled = false
                    val leftAxis = lineChart.axisLeft
                    leftAxis.axisMinimum = 0f
                    leftAxis.axisMaximum = 100f

                    lineChart.setTouchEnabled(true)
                    lineChart.setPinchZoom(true)

                    lineChart.description.text = "Time"
                    lineChart.setNoDataText("No data yet!")
                    lineChart.data = LineData(vl,vl_l)
                    lineChart.animateY(1800, Easing.EaseInExpo)
                }
                override fun onCancelled(databaseError: DatabaseError) {
                    Log.e(LOG_TAG, "Database error", databaseError.toException())
                }
            })
        }


        //generating feet temp history
        val temp_his = findViewById<Button>(R.id.temp_plot)
        temp_his.setOnClickListener {

            val ref = FirebaseDatabase.getInstance().getReference("postlist")

            ref.addListenerForSingleValueEvent(object : ValueEventListener {
                override fun onDataChange(data: DataSnapshot) {
                    val entries2 = ArrayList<Entry>()
                    for (childSnapshot in data.children) {
                        val xValue2 = childSnapshot.child("time").getValue(Float::class.java)
                        val yValue2 = childSnapshot.child("temperature").getValue(Float::class.java)
                        if(xValue2 != null && yValue2 != null){
                            entries2.add(Entry(xValue2, yValue2))
                        }
                    }
                    val vl2 = LineDataSet(entries2, "Feet temperature history")

                    vl2.setDrawValues(false)
                    vl2.setDrawFilled(true)
                    vl2.lineWidth = 3f
                    vl2.color = Color.BLACK
                    vl2.fillColor = R.color.lightred
                    vl2.fillAlpha = R.color.pink

                    val lineChart2 = findViewById<com.github.mikephil.charting.charts.LineChart>(R.id.temp_lineChart)
                    lineChart2.xAxis.labelRotationAngle = 0f

                    lineChart2.axisRight.isEnabled = false
                    val leftAxis2 = lineChart2.axisLeft
                    leftAxis2.axisMinimum = 0f
                    leftAxis2.axisMaximum = 40f

                    lineChart2.setTouchEnabled(true)
                    lineChart2.setPinchZoom(true)

                    lineChart2.description.text = "Time"
                    lineChart2.setNoDataText("No data yet!")
                    lineChart2.data = LineData(vl2)
                    lineChart2.animateY(1800, Easing.EaseInExpo)
                }
                override fun onCancelled(databaseError: DatabaseError) {
                    Log.e(LOG_TAG, "Database error", databaseError.toException())
                }
            })
        }
    }
}