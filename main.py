#---Импорты---
import sys
import os
import io
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QMessageBox, QFileDialog, QHeaderView, QTableWidgetItem
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt, QTimer
import csv
import sqlite3
from datetime import datetime, timedelta

#---Константы---
main_template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>MainWindow</class>
 <widget class="QMainWindow" name="MainWindow">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>467</width>
    <height>155</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>467</width>
    <height>155</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>You Can</string>
  </property>
  <widget class="QWidget" name="centralwidget">
   <layout class="QHBoxLayout" name="horizontalLayout">
    <property name="spacing">
     <number>20</number>
    </property>
    <item>
     <widget class="QFrame" name="frame">
      <property name="frameShape">
       <enum>QFrame::Shape::NoFrame</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout">
       <item>
        <widget class="QLCDNumber" name="smoked_lcd"/>
       </item>
       <item>
        <widget class="QLabel" name="smoked_label">
         <property name="text">
          <string>Сигарет выкурено</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
    <item>
     <widget class="QFrame" name="frame_2">
      <property name="frameShape">
       <enum>QFrame::Shape::NoFrame</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout_2">
       <item>
        <widget class="QPushButton" name="smoke_btn">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Expanding">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="text">
          <string>Выкурил(-а) сигарету</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
    <item>
     <widget class="QFrame" name="frame_3">
      <property name="frameShape">
       <enum>QFrame::Shape::NoFrame</enum>
      </property>
      <property name="frameShadow">
       <enum>QFrame::Shadow::Raised</enum>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout_3">
       <item>
        <widget class="QLabel" name="label_3">
         <property name="text">
          <string>Прочие расходы</string>
         </property>
        </widget>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_2">
         <item>
          <widget class="QDoubleSpinBox" name="sum_doublespinbox">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="maximum">
            <double>1000000.000000000000000</double>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_2">
           <property name="text">
            <string>рублей</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <widget class="QPushButton" name="spend_btn">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Minimum" vsizetype="Preferred">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="text">
          <string>Потратить</string>
         </property>
        </widget>
       </item>
      </layout>
     </widget>
    </item>
   </layout>
  </widget>
  <widget class="QMenuBar" name="menubar">
   <property name="geometry">
    <rect>
     <x>0</x>
     <y>0</y>
     <width>467</width>
     <height>22</height>
    </rect>
   </property>
   <widget class="QMenu" name="menu_settings">
    <property name="title">
     <string>Настройки</string>
    </property>
    <addaction name="action_open_settings"/>
   </widget>
   <widget class="QMenu" name="menu_lk">
    <property name="title">
     <string>Личный кабинет</string>
    </property>
    <addaction name="action_open_lk"/>
   </widget>
   <addaction name="menu_lk"/>
   <addaction name="menu_settings"/>
  </widget>
  <widget class="QStatusBar" name="statusbar"/>
  <action name="action_open_lk">
   <property name="text">
    <string>Личный кабинет</string>
   </property>
  </action>
  <action name="action_open_settings">
   <property name="text">
    <string>Настройки</string>
   </property>
  </action>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

'''!!!!!!!!!!'''
main_style_dark = '''
    QMainWindow {
        background-color: #121212;
    }
'''
main_style_light = ''''''

register_template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>444</width>
    <height>278</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>444</width>
    <height>278</height>
   </size>
  </property>
  <property name="maximumSize">
   <size>
    <width>444</width>
    <height>425</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>You Can - Введите ваши данные</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout">
     <property name="sizeConstraint">
      <enum>QLayout::SizeConstraint::SetDefaultConstraint</enum>
     </property>
     <item>
      <widget class="QLabel" name="label">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
       <property name="minimumSize">
        <size>
         <width>78</width>
         <height>16</height>
        </size>
       </property>
       <property name="text">
        <string>Как Вас зовут?</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QLineEdit" name="name_lineedit">
       <property name="minimumSize">
        <size>
         <width>333</width>
         <height>22</height>
        </size>
       </property>
      </widget>
     </item>
    </layout>
   </item>
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout_2">
     <property name="sizeConstraint">
      <enum>QLayout::SizeConstraint::SetDefaultConstraint</enum>
     </property>
     <item>
      <widget class="QLabel" name="label_2">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
       <property name="minimumSize">
        <size>
         <width>98</width>
         <height>16</height>
        </size>
       </property>
       <property name="text">
        <string>Сколько Вам лет?</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QSpinBox" name="age_spinbox">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
       <property name="minimumSize">
        <size>
         <width>313</width>
         <height>22</height>
        </size>
       </property>
       <property name="maximum">
        <number>120</number>
       </property>
      </widget>
     </item>
    </layout>
   </item>
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout_3">
     <property name="sizeConstraint">
      <enum>QLayout::SizeConstraint::SetDefaultConstraint</enum>
     </property>
     <item>
      <widget class="QLabel" name="label_3">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
       <property name="minimumSize">
        <size>
         <width>84</width>
         <height>16</height>
        </size>
       </property>
       <property name="text">
        <string>Что Вы курите?</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QComboBox" name="smoke_variant_combobox">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
       <property name="minimumSize">
        <size>
         <width>327</width>
         <height>22</height>
        </size>
       </property>
       <item>
        <property name="text">
         <string>Сигареты</string>
        </property>
       </item>
       <item>
        <property name="text">
         <string>Самодельные сигареты (самокрутки)</string>
        </property>
       </item>
       <item>
        <property name="text">
         <string>Системы нагревания табака (СНТ)</string>
        </property>
       </item>
       <item>
        <property name="text">
         <string>Электронные сигареты</string>
        </property>
       </item>
      </widget>
     </item>
    </layout>
   </item>
   <item>
    <widget class="QWidget" name="cigarette_widget" native="true">
     <property name="sizePolicy">
      <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
       <horstretch>0</horstretch>
       <verstretch>0</verstretch>
      </sizepolicy>
     </property>
     <property name="minimumSize">
      <size>
       <width>419</width>
       <height>95</height>
      </size>
     </property>
     <widget class="QWidget" name="verticalLayoutWidget_2">
      <property name="geometry">
       <rect>
        <x>0</x>
        <y>0</y>
        <width>421</width>
        <height>94</height>
       </rect>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout_2">
       <property name="spacing">
        <number>10</number>
       </property>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_4">
         <item>
          <widget class="QLabel" name="label_4">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Maximum" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>94</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>В день Вы курите</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QSpinBox" name="cigarettes_per_day_spinbox">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>156</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <number>5000</number>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_5">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>155</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>сигарет</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_5">
         <item>
          <widget class="QLabel" name="label_6">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>141</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>Одна пачка сигарет стоит</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QDoubleSpinBox" name="cigarette_cost_doublespinbox">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>132</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <double>1000000.000000000000000</double>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_7">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>132</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>рублей</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_6">
         <item>
          <widget class="QLabel" name="label_8">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Maximum" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>79</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>В одной пачке</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QSpinBox" name="cigarette_count_spinbox">
           <property name="minimumSize">
            <size>
             <width>163</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <number>5000</number>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_9">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>163</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>сигарет</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </widget>
   </item>
   <item>
    <widget class="QWidget" name="custom_widget" native="true">
     <property name="sizePolicy">
      <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
       <horstretch>0</horstretch>
       <verstretch>0</verstretch>
      </sizepolicy>
     </property>
     <property name="minimumSize">
      <size>
       <width>419</width>
       <height>241</height>
      </size>
     </property>
     <widget class="QWidget" name="verticalLayoutWidget_3">
      <property name="geometry">
       <rect>
        <x>-1</x>
        <y>-1</y>
        <width>431</width>
        <height>241</height>
       </rect>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout_3">
       <property name="spacing">
        <number>10</number>
       </property>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_7">
         <item>
          <widget class="QLabel" name="label_10">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>94</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>В день Вы курите</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QSpinBox" name="customs_per_day_spinbox">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>161</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <number>5000</number>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_11">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>160</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>самокруток</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_8">
         <item>
          <widget class="QLabel" name="label_12">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>134</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>Один кисет табака стоит</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QDoubleSpinBox" name="tobacco_cost_doublespinbox">
           <property name="minimumSize">
            <size>
             <width>141</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <double>1000000.000000000000000</double>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_13">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>140</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>рублей</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_9">
         <item>
          <widget class="QLabel" name="label_14">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>46</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>В кисете</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QSpinBox" name="tobacco_count_spinbox">
           <property name="minimumSize">
            <size>
             <width>185</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <number>5000</number>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_15">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>184</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>грамм табака</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_10">
         <item>
          <widget class="QLabel" name="label_16">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>176</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>Пачка сигаретной бумаги стоит</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QDoubleSpinBox" name="paper_cost_doublespinbox">
           <property name="minimumSize">
            <size>
             <width>120</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <double>1000000.000000000000000</double>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_17">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>119</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>рублей</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_11">
         <item>
          <widget class="QLabel" name="label_18">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>42</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>В пачке</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QSpinBox" name="paper_count_spinbox">
           <property name="minimumSize">
            <size>
             <width>187</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <number>5000</number>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_19">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>186</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>бумажек</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_12">
         <item>
          <widget class="QLabel" name="label_20">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>161</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>Пачка фильтров/типок стоит</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QDoubleSpinBox" name="filter_cost_doublespinbox">
           <property name="minimumSize">
            <size>
             <width>127</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <double>1000000.000000000000000</double>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_21">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>127</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>рублей</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_13">
         <item>
          <widget class="QLabel" name="label_22">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>42</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>В пачке</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QSpinBox" name="filter_count_spinbox">
           <property name="minimumSize">
            <size>
             <width>187</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <number>5000</number>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_23">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>186</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>фильтров/типок</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </widget>
   </item>
   <item>
    <widget class="QWidget" name="stic_widget" native="true">
     <property name="sizePolicy">
      <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
       <horstretch>0</horstretch>
       <verstretch>0</verstretch>
      </sizepolicy>
     </property>
     <property name="minimumSize">
      <size>
       <width>419</width>
       <height>90</height>
      </size>
     </property>
     <widget class="QWidget" name="verticalLayoutWidget_4">
      <property name="geometry">
       <rect>
        <x>-1</x>
        <y>-1</y>
        <width>431</width>
        <height>91</height>
       </rect>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout_4">
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_16">
         <item>
          <widget class="QLabel" name="label_28">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="text">
            <string>В день Вы курите</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QSpinBox" name="stics_per_day_spinbox">
           <property name="minimumSize">
            <size>
             <width>161</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <number>5000</number>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_29">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>160</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>стиков</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_14">
         <item>
          <widget class="QLabel" name="label_24">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>107</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>Пачка стиков стоит</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QDoubleSpinBox" name="stic_cost_doublespinbox">
           <property name="minimumSize">
            <size>
             <width>154</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <double>1000000.000000000000000</double>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_25">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>154</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>рублей</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_15">
         <item>
          <widget class="QLabel" name="label_26">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>42</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>В пачке</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QSpinBox" name="stic_count_spinbox">
           <property name="minimumSize">
            <size>
             <width>187</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <number>5000</number>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_27">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>186</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>стиков</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
      </layout>
     </widget>
    </widget>
   </item>
   <item>
    <widget class="QWidget" name="vape_widget" native="true">
     <property name="sizePolicy">
      <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
       <horstretch>0</horstretch>
       <verstretch>0</verstretch>
      </sizepolicy>
     </property>
     <property name="minimumSize">
      <size>
       <width>419</width>
       <height>125</height>
      </size>
     </property>
     <property name="maximumSize">
      <size>
       <width>100000</width>
       <height>100000</height>
      </size>
     </property>
     <widget class="QWidget" name="layoutWidget">
      <property name="geometry">
       <rect>
        <x>1</x>
        <y>1</y>
        <width>421</width>
        <height>220</height>
       </rect>
      </property>
      <layout class="QVBoxLayout" name="verticalLayout_7" stretch="0,0,0,0">
       <property name="spacing">
        <number>10</number>
       </property>
       <property name="sizeConstraint">
        <enum>QLayout::SizeConstraint::SetMaximumSize</enum>
       </property>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_17">
         <property name="sizeConstraint">
          <enum>QLayout::SizeConstraint::SetFixedSize</enum>
         </property>
         <item>
          <widget class="QLabel" name="label_30">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>99</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>В день Вы делаете</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QSpinBox" name="puffs_per_day_spinbox">
           <property name="minimumSize">
            <size>
             <width>143</width>
             <height>22</height>
            </size>
           </property>
           <property name="maximum">
            <number>2000</number>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QLabel" name="label_31">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>143</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>затяжек</string>
           </property>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <layout class="QHBoxLayout" name="horizontalLayout_18">
         <property name="sizeConstraint">
          <enum>QLayout::SizeConstraint::SetFixedSize</enum>
         </property>
         <item>
          <widget class="QLabel" name="label_32">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Maximum" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>87</width>
             <height>16</height>
            </size>
           </property>
           <property name="text">
            <string>Вы используете</string>
           </property>
          </widget>
         </item>
         <item>
          <widget class="QComboBox" name="vape_variant_combobox">
           <property name="sizePolicy">
            <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
             <horstretch>0</horstretch>
             <verstretch>0</verstretch>
            </sizepolicy>
           </property>
           <property name="minimumSize">
            <size>
             <width>320</width>
             <height>22</height>
            </size>
           </property>
           <item>
            <property name="text">
             <string>Одноразовый под</string>
            </property>
           </item>
           <item>
            <property name="text">
             <string>Многоразовый под или мод</string>
            </property>
           </item>
          </widget>
         </item>
        </layout>
       </item>
       <item>
        <widget class="QWidget" name="vape1_widget" native="true">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Preferred" vsizetype="Maximum">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="minimumSize">
          <size>
           <width>419</width>
           <height>60</height>
          </size>
         </property>
         <widget class="QWidget" name="verticalLayoutWidget_5">
          <property name="geometry">
           <rect>
            <x>-1</x>
            <y>-1</y>
            <width>421</width>
            <height>60</height>
           </rect>
          </property>
          <layout class="QVBoxLayout" name="verticalLayout_5">
           <property name="spacing">
            <number>10</number>
           </property>
           <property name="sizeConstraint">
            <enum>QLayout::SizeConstraint::SetDefaultConstraint</enum>
           </property>
           <item>
            <layout class="QHBoxLayout" name="horizontalLayout_19">
             <item>
              <widget class="QLabel" name="label_33">
               <property name="sizePolicy">
                <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="minimumSize">
                <size>
                 <width>55</width>
                 <height>22</height>
                </size>
               </property>
               <property name="text">
                <string>Под стоит</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="onepod_cost_doublespinbox">
               <property name="minimumSize">
                <size>
                 <width>165</width>
                 <height>22</height>
                </size>
               </property>
               <property name="maximum">
                <double>1000000.000000000000000</double>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QLabel" name="label_34">
               <property name="sizePolicy">
                <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="minimumSize">
                <size>
                 <width>165</width>
                 <height>22</height>
                </size>
               </property>
               <property name="text">
                <string>рублей</string>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item>
            <layout class="QHBoxLayout" name="horizontalLayout_20">
             <item>
              <widget class="QLabel" name="label_35">
               <property name="sizePolicy">
                <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="minimumSize">
                <size>
                 <width>98</width>
                 <height>22</height>
                </size>
               </property>
               <property name="text">
                <string>Под рассчитан на</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QSpinBox" name="onepod_count_spinbox">
               <property name="minimumSize">
                <size>
                 <width>144</width>
                 <height>22</height>
                </size>
               </property>
               <property name="minimum">
                <number>0</number>
               </property>
               <property name="maximum">
                <number>99999</number>
               </property>
               <property name="singleStep">
                <number>1</number>
               </property>
               <property name="value">
                <number>0</number>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QLabel" name="label_36">
               <property name="sizePolicy">
                <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="minimumSize">
                <size>
                 <width>143</width>
                 <height>22</height>
                </size>
               </property>
               <property name="text">
                <string>затяжек</string>
               </property>
              </widget>
             </item>
            </layout>
           </item>
          </layout>
         </widget>
        </widget>
       </item>
       <item>
        <widget class="QWidget" name="vape2_widget" native="true">
         <property name="sizePolicy">
          <sizepolicy hsizetype="Preferred" vsizetype="Maximum">
           <horstretch>0</horstretch>
           <verstretch>0</verstretch>
          </sizepolicy>
         </property>
         <property name="minimumSize">
          <size>
           <width>419</width>
           <height>60</height>
          </size>
         </property>
         <widget class="QWidget" name="verticalLayoutWidget_6">
          <property name="geometry">
           <rect>
            <x>-1</x>
            <y>-1</y>
            <width>421</width>
            <height>60</height>
           </rect>
          </property>
          <layout class="QVBoxLayout" name="verticalLayout_6">
           <property name="spacing">
            <number>10</number>
           </property>
           <property name="sizeConstraint">
            <enum>QLayout::SizeConstraint::SetDefaultConstraint</enum>
           </property>
           <item>
            <layout class="QHBoxLayout" name="horizontalLayout_21">
             <item>
              <widget class="QLabel" name="label_37">
               <property name="sizePolicy">
                <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="minimumSize">
                <size>
                 <width>131</width>
                 <height>22</height>
                </size>
               </property>
               <property name="text">
                <string>Флакон жидкости стоит</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="liquid_cost_doublespinbox">
               <property name="minimumSize">
                <size>
                 <width>127</width>
                 <height>22</height>
                </size>
               </property>
               <property name="maximum">
                <double>1000000.000000000000000</double>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QLabel" name="label_38">
               <property name="sizePolicy">
                <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="minimumSize">
                <size>
                 <width>127</width>
                 <height>22</height>
                </size>
               </property>
               <property name="text">
                <string>рублей</string>
               </property>
              </widget>
             </item>
            </layout>
           </item>
           <item>
            <layout class="QHBoxLayout" name="horizontalLayout_22">
             <item>
              <widget class="QLabel" name="label_39">
               <property name="sizePolicy">
                <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="minimumSize">
                <size>
                 <width>92</width>
                 <height>22</height>
                </size>
               </property>
               <property name="text">
                <string>Объем флакона:</string>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QDoubleSpinBox" name="liquid_count_doublespinbox">
               <property name="minimumSize">
                <size>
                 <width>147</width>
                 <height>22</height>
                </size>
               </property>
               <property name="decimals">
                <number>1</number>
               </property>
               <property name="maximum">
                <double>5000.000000000000000</double>
               </property>
              </widget>
             </item>
             <item>
              <widget class="QLabel" name="label_40">
               <property name="sizePolicy">
                <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
                 <horstretch>0</horstretch>
                 <verstretch>0</verstretch>
                </sizepolicy>
               </property>
               <property name="minimumSize">
                <size>
                 <width>146</width>
                 <height>22</height>
                </size>
               </property>
               <property name="text">
                <string>мл</string>
               </property>
              </widget>
             </item>
            </layout>
           </item>
          </layout>
         </widget>
        </widget>
       </item>
      </layout>
     </widget>
    </widget>
   </item>
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout_200">
     <item>
      <widget class="QLabel" name="label_200">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
       <property name="minimumSize">
        <size>
         <width>231</width>
         <height>16</height>
        </size>
       </property>
       <property name="text">
        <string>Загрузить фото профиля (необязательно)</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="load_photo_btn">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
       <property name="minimumSize">
        <size>
         <width>93</width>
         <height>24</height>
        </size>
       </property>
       <property name="text">
        <string>Загрузить фото</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QLabel" name="is_photo_loaded_label">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
       <property name="minimumSize">
        <size>
         <width>76</width>
         <height>16</height>
        </size>
       </property>
       <property name="text">
        <string>Не загружено</string>
       </property>
      </widget>
     </item>
    </layout>
   </item>
   <item>
    <widget class="QPushButton" name="finish_btn">
     <property name="minimumSize">
      <size>
       <width>419</width>
       <height>24</height>
      </size>
     </property>
     <property name="text">
      <string>Готово</string>
     </property>
    </widget>
   </item>
   <item>
    <spacer name="verticalSpacer">
     <property name="orientation">
      <enum>Qt::Orientation::Vertical</enum>
     </property>
     <property name="sizeHint" stdset="0">
      <size>
       <width>20</width>
       <height>40</height>
      </size>
     </property>
    </spacer>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

'''!!!!!!!!!!'''
register_style_dark = '''
    QWidget {
        background-color: #121212;
    }
'''
register_style_light = ''''''

settings_template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>275</width>
    <height>305</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>275</width>
    <height>305</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>You Can - Настройки</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout">
   <item>
    <widget class="QPushButton" name="change_theme_btn">
     <property name="text">
      <string>Светлая тема</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QPushButton" name="change_data_btn">
     <property name="sizePolicy">
      <sizepolicy hsizetype="Minimum" vsizetype="Fixed">
       <horstretch>0</horstretch>
       <verstretch>0</verstretch>
      </sizepolicy>
     </property>
     <property name="text">
      <string>Изменить данные</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QLabel" name="label">
     <property name="sizePolicy">
      <sizepolicy hsizetype="Preferred" vsizetype="Fixed">
       <horstretch>0</horstretch>
       <verstretch>0</verstretch>
      </sizepolicy>
     </property>
     <property name="text">
      <string>Отображаемые в статистике характеристики:</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QCheckBox" name="smoked_cigarettes_checkbox">
     <property name="text">
      <string>Выкуренные сигареты</string>
     </property>
     <property name="checked">
      <bool>true</bool>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QCheckBox" name="unsmoked_cigarettes_checkbox">
     <property name="text">
      <string>Невыкуренные сигареты</string>
     </property>
     <property name="checked">
      <bool>true</bool>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QCheckBox" name="smoked_puffs_checkbox">
     <property name="text">
      <string>Сделанные затяжки</string>
     </property>
     <property name="checked">
      <bool>true</bool>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QCheckBox" name="unsmoked_puffs_checkbox">
     <property name="text">
      <string>Несделанные затяжки</string>
     </property>
     <property name="checked">
      <bool>true</bool>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QCheckBox" name="spent_checkbox">
     <property name="text">
      <string>Потрачено, руб</string>
     </property>
     <property name="checked">
      <bool>true</bool>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QCheckBox" name="unspent_checkbox">
     <property name="text">
      <string>Сэкономлено, руб</string>
     </property>
     <property name="checked">
      <bool>true</bool>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QCheckBox" name="progress_checkbox">
     <property name="text">
      <string>Прогресс</string>
     </property>
     <property name="checked">
      <bool>true</bool>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QPushButton" name="reset_btn">
     <property name="text">
      <string>Сбросить статистику и историю</string>
     </property>
    </widget>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

'''!!!!!!!!!!'''
settings_style_dark = '''
    QWidget {
            background-color: #121212;
    }
'''
settings_style_light = ''''''

lk_template = '''<?xml version="1.0" encoding="UTF-8"?>
<ui version="4.0">
 <class>Form</class>
 <widget class="QWidget" name="Form">
  <property name="geometry">
   <rect>
    <x>0</x>
    <y>0</y>
    <width>750</width>
    <height>688</height>
   </rect>
  </property>
  <property name="minimumSize">
   <size>
    <width>750</width>
    <height>688</height>
   </size>
  </property>
  <property name="windowTitle">
   <string>You Can - Личный кабинет</string>
  </property>
  <layout class="QVBoxLayout" name="verticalLayout" stretch="0,0,0,0,0,0,1,0,0">
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout" stretch="0,1">
     <property name="sizeConstraint">
      <enum>QLayout::SizeConstraint::SetDefaultConstraint</enum>
     </property>
     <item>
      <widget class="QLabel" name="photo_label">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Fixed" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
       <property name="minimumSize">
        <size>
         <width>100</width>
         <height>100</height>
        </size>
       </property>
       <property name="maximumSize">
        <size>
         <width>100</width>
         <height>100</height>
        </size>
       </property>
       <property name="text">
        <string/>
       </property>
       <property name="scaledContents">
        <bool>false</bool>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QWidget" name="widget" native="true">
       <property name="sizePolicy">
        <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
         <horstretch>0</horstretch>
         <verstretch>0</verstretch>
        </sizepolicy>
       </property>
       <layout class="QVBoxLayout" name="verticalLayout_3">
        <item>
         <widget class="QLabel" name="name_label">
          <property name="sizePolicy">
           <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
            <horstretch>0</horstretch>
            <verstretch>0</verstretch>
           </sizepolicy>
          </property>
          <property name="text">
           <string/>
          </property>
          <property name="alignment">
           <set>Qt::AlignmentFlag::AlignLeading|Qt::AlignmentFlag::AlignLeft|Qt::AlignmentFlag::AlignVCenter</set>
          </property>
         </widget>
        </item>
        <item>
         <widget class="QLabel" name="age_label">
          <property name="sizePolicy">
           <sizepolicy hsizetype="Expanding" vsizetype="Fixed">
            <horstretch>0</horstretch>
            <verstretch>0</verstretch>
           </sizepolicy>
          </property>
          <property name="text">
           <string/>
          </property>
         </widget>
        </item>
        <item>
         <spacer name="verticalSpacer">
          <property name="orientation">
           <enum>Qt::Orientation::Vertical</enum>
          </property>
          <property name="sizeHint" stdset="0">
           <size>
            <width>20</width>
            <height>40</height>
           </size>
          </property>
         </spacer>
        </item>
       </layout>
      </widget>
     </item>
    </layout>
   </item>
   <item>
    <widget class="QLabel" name="label_3">
     <property name="text">
      <string>Статистика</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QTableWidget" name="statistic_tablewidget">
     <property name="sizePolicy">
      <sizepolicy hsizetype="Expanding" vsizetype="Expanding">
       <horstretch>0</horstretch>
       <verstretch>0</verstretch>
      </sizepolicy>
     </property>
     <property name="minimumSize">
      <size>
       <width>0</width>
       <height>175</height>
      </size>
     </property>
     <property name="maximumSize">
      <size>
       <width>16777215</width>
       <height>229</height>
      </size>
     </property>
     <attribute name="horizontalHeaderCascadingSectionResizes">
      <bool>false</bool>
     </attribute>
     <attribute name="horizontalHeaderStretchLastSection">
      <bool>true</bool>
     </attribute>
     <column>
      <property name="text">
       <string>Название характеристики</string>
      </property>
     </column>
     <column>
      <property name="text">
       <string>Значение</string>
      </property>
     </column>
    </widget>
   </item>
   <item>
    <widget class="QLabel" name="label">
     <property name="text">
      <string>Скачать статистику</string>
     </property>
    </widget>
   </item>
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout_2">
     <item>
      <widget class="QPushButton" name="statistic_txt_btn">
       <property name="text">
        <string>.txt</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="statistic_csv_btn">
       <property name="text">
        <string>.csv</string>
       </property>
      </widget>
     </item>
    </layout>
   </item>
   <item>
    <widget class="QLabel" name="label_4">
     <property name="text">
      <string>История</string>
     </property>
    </widget>
   </item>
   <item>
    <widget class="QTableWidget" name="history_tablewidget">
     <property name="minimumSize">
      <size>
       <width>0</width>
       <height>229</height>
      </size>
     </property>
     <property name="maximumSize">
      <size>
       <width>16777215</width>
       <height>229</height>
      </size>
     </property>
     <attribute name="horizontalHeaderStretchLastSection">
      <bool>true</bool>
     </attribute>
     <column>
      <property name="text">
       <string>Дата</string>
      </property>
     </column>
     <column>
      <property name="text">
       <string>Выкурено сигарет</string>
      </property>
     </column>
     <column>
      <property name="text">
       <string>Не выкурено сигарет</string>
      </property>
     </column>
     <column>
      <property name="text">
       <string>Потрачено, руб</string>
      </property>
     </column>
     <column>
      <property name="text">
       <string>Сэкономлено, руб</string>
      </property>
     </column>
    </widget>
   </item>
   <item>
    <widget class="QLabel" name="label_2">
     <property name="text">
      <string>Скачать историю</string>
     </property>
    </widget>
   </item>
   <item>
    <layout class="QHBoxLayout" name="horizontalLayout_3">
     <item>
      <widget class="QPushButton" name="history_txt_btn">
       <property name="text">
        <string>.txt</string>
       </property>
      </widget>
     </item>
     <item>
      <widget class="QPushButton" name="history_csv_btn">
       <property name="text">
        <string>.csv</string>
       </property>
      </widget>
     </item>
    </layout>
   </item>
  </layout>
 </widget>
 <resources/>
 <connections/>
</ui>
'''

'''!!!!!!!!!!'''
lk_style_dark = '''
    QWidget {
        background-color: #121212;
    }
'''
lk_style_light = ''''''


#---Класс главного окна---
class Main(QMainWindow):
    def __init__(self):
        super().__init__()

        f = io.StringIO(main_template)
        uic.loadUi(f, self)

        #-Создание и заполнение таблиц, если их нет-
        self.con = sqlite3.connect('You Can/youcan.db')
        cur = self.con.cursor()
        cur.execute('''CREATE TABLE IF NOT EXISTS table_history (
                        date DATE PRIMARY KEY,
                        smoked INTEGER,
                        unsmoked INTEGER,
                        spent_money REAL,
                        unspent_money REAL
                    )''')
        cur.execute('''CREATE TABLE IF NOT EXISTS table_statistic (
                        name_record TEXT PRIMARY KEY,
                        value REAL
                    )''')
        cur.execute('''INSERT OR IGNORE INTO table_statistic(name_record, value) VALUES
                        ("last_updated_date", 0.0),
                        ("smoked_cigarettes", 0.0),
                        ("unsmoked_cigarettes", 0.0),
                        ("smoked_puffs", 0.0),
                        ("unsmoked_puffs", 0.0),
                        ("spent_money", 0.0),
                        ("unspent_money", 0.0),
                        ("progress", 0.0)
                    ''')
        cur.execute('''CREATE TABLE IF NOT EXISTS table_user (
                        id INTEGER PRIMARY KEY,
                        name TEXT,
                        age INTEGER,
                        smoke_variant TEXT,
                        cigarettes_per_day INTEGER,
                        cigarette_cost REAL,
                        cigarette_count INTEGER,
                        customs_per_day INTEGER,
                        tobacco_cost REAL,
                        tobacco_count INTEGER,
                        paper_cost REAL,
                        paper_count INTEGER,
                        filter_cost REAL,
                        filter_count INTEGER,
                        stics_per_day INTEGER,
                        stic_cost REAL,
                        stic_count INTEGER,
                        puffs_per_day INTEGER,
                        vape_variant TEXT,
                        onepod_cost REAL,
                        onepod_count INTEGER,
                        liquid_cost REAL,
                        liquid_count REAL,
                        photo_path TEXT
                    )''')
        cur.execute('''INSERT OR IGNORE INTO table_user(id, name, age, smoke_variant, cigarettes_per_day,
                            cigarette_cost, cigarette_count, customs_per_day, tobacco_cost, tobacco_count, paper_cost,
                            paper_count, filter_cost, filter_count, stics_per_day, stic_cost, stic_count, puffs_per_day,
                            vape_variant, onepod_cost, onepod_count, liquid_cost, liquid_count, photo_path)
                            VALUES (0, "", 0, "Сигареты", 0, 0.0, 0, 0, 0.0, 0, 0.0, 0, 0.0, 0, 0, 0.0, 0, 0,
                            "Одноразовый под", 0.0, 0, 0.0, 0.0, "d:\VS Code\You Can\images\default_photo.png")
                    ''')
        cur.execute('''CREATE TABLE IF NOT EXISTS table_settings (
                        name_set TEXT PRIMARY KEY,
                        value INTEGER
                    )''')
        cur.execute('''INSERT OR IGNORE INTO table_settings(name_set, value) VALUES
                        ("smoked_cigarettes", 1),
                        ("unsmoked_cigarettes", 1),
                        ("smoked_puffs", 1),
                        ("unsmoked_puffs", 1),
                        ("spent_money", 1),
                        ("unspent_money", 1),
                        ("progress", 1),
                        ("theme", 0)
                    ''')
        self.con.commit()

        self.initUI()

    '''!!!!!!!!!!'''
    def initUI(self):
        cur = self.con.cursor()
        self.name = cur.execute('''SELECT name FROM table_user''').fetchall()[0][0]
        self.age = cur.execute('''SELECT age FROM table_user''').fetchall()[0][0]
        self.smoke_variant = cur.execute('''SELECT smoke_variant FROM table_user''').fetchall()[0][0]
        self.cigarettes_per_day = cur.execute('''SELECT cigarettes_per_day FROM table_user''').fetchall()[0][0]
        self.cigarette_cost = cur.execute('''SELECT cigarette_cost FROM table_user''').fetchall()[0][0]
        self.cigarette_count = cur.execute('''SELECT cigarette_count FROM table_user''').fetchall()[0][0]
        self.customs_per_day = cur.execute('''SELECT customs_per_day FROM table_user''').fetchall()[0][0]
        self.tobacco_cost = cur.execute('''SELECT tobacco_cost FROM table_user''').fetchall()[0][0]
        self.tobacco_count = cur.execute('''SELECT tobacco_count FROM table_user''').fetchall()[0][0]
        self.paper_cost = cur.execute('''SELECT paper_cost FROM table_user''').fetchall()[0][0]
        self.paper_count = cur.execute('''SELECT paper_count FROM table_user''').fetchall()[0][0]
        self.filter_cost = cur.execute('''SELECT filter_cost FROM table_user''').fetchall()[0][0]
        self.filter_count = cur.execute('''SELECT filter_count FROM table_user''').fetchall()[0][0]
        self.stics_per_day = cur.execute('''SELECT stics_per_day FROM table_user''').fetchall()[0][0]
        self.stic_cost = cur.execute('''SELECT stic_cost FROM table_user''').fetchall()[0][0]
        self.stic_count = cur.execute('''SELECT stic_count FROM table_user''').fetchall()[0][0]
        self.puffs_per_day = cur.execute('''SELECT puffs_per_day FROM table_user''').fetchall()[0][0]
        self.vape_variant = cur.execute('''SELECT vape_variant FROM table_user''').fetchall()[0][0]
        self.onepod_cost = cur.execute('''SELECT onepod_cost FROM table_user''').fetchall()[0][0]
        self.onepod_count = cur.execute('''SELECT onepod_count FROM table_user''').fetchall()[0][0]
        self.liquid_cost = cur.execute('''SELECT liquid_cost FROM table_user''').fetchall()[0][0]
        self.liquid_count = cur.execute('''SELECT liquid_count FROM table_user''').fetchall()[0][0]
        self.photo_path = cur.execute('''SELECT photo_path FROM table_user''').fetchall()[0][0]
        self.theme = cur.execute('''SELECT value FROM table_settings WHERE name_set = "theme"''').fetchall()[0][0]
        self.active_statistics = [e[0] for e in cur.execute('''SELECT name_set FROM table_settings
                                                            WHERE name_set != "theme" AND value = 1''').fetchall()]

        #-Проверка: все ли обязательные значения в таблице пользователя заполнены-
        f = 0
        if self.name == '' or self.age == 0:
            f = 1
        if self.smoke_variant == 'Сигареты':
            if self.cigarettes_per_day == 0:
                f = 1
            if self.cigarette_cost != 0 and self.cigarette_count == 0:
                f = 1
        elif self.smoke_variant == 'Самодельные сигареты (самокрутки)':
            if self.customs_per_day == 0:
                f = 1
            if self.tobacco_cost != 0 and self.tobacco_count == 0:
                f = 1
            if self.paper_cost != 0 and self.paper_count == 0:
                f = 1
            if self.filter_cost != 0 and self.filter_count == 0:
                f = 1
        elif self.smoke_variant == 'Системы нагревания табака (СНТ)':
            if self.stics_per_day == 0:
                f = 1
            if self.stic_cost != 0 and self.stic_count == 0:
                f = 1
        elif self.smoke_variant == 'Электронные сигареты':
            if self.puffs_per_day == 0:
                f = 1
            if self.vape_variant == 'Одноразовый под':
                if self.onepod_cost != 0 and self.onepod_count == 0:
                    f = 1
            elif self.vape_variant == 'Многоразовый под или мод':
                if self.liquid_cost != 0 and self.liquid_count == 0:
                    f = 1
            else:
                f = 1
        else:
            f = 1

        self.register = Register(self)
        self.settings = Settings(self)
        self.lk = Lk(self)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_date)
        self.timer.start(60000)

        if self.smoke_variant == 'Сигареты' or self.smoke_variant == 'Самодельные сигареты (самокрутки)':
            self.smoked_label.setText('Сигарет выкурено')
            self.smoke_btn.setText('Выкурил(-а) сигарету')
        elif self.smoke_variant == 'Системы нагревания табака (СНТ)':
            self.smoked_label.setText('Стиков выкурено')
            self.smoke_btn.setText('Выкурил(-а) стик')
        elif self.smoke_variant == 'Электронные сигареты':
            self.smoked_label.setText('Затяжек сделано')
            self.smoke_btn.setText('Сделал(-а) затяжку')

        self.action_open_settings.triggered.connect(self.settings.show)
        self.action_open_lk.triggered.connect(self.lk.show)

        self.smoke_btn.clicked.connect(self.smoke)
        self.spend_btn.clicked.connect(self.spend)

        #self.setStyleSheet(main_style_dark)

        #-Если нет, открытие окна регистрации-
        if f:
            self.register.show()
        else:
            self.check_date()
            self.smoked_lcd.display(cur.execute('''SELECT smoked FROM table_history
                                            WHERE date = ?''',
                                            (datetime.strftime(datetime.today(), '%Y-%m-%d'),)).fetchone()[0])
            self.show()

    def set_settings(self):
        cur = self.con.cursor()
        old_smoke_variant = ''
        if self.smoke_variant != cur.execute('''SELECT smoke_variant FROM table_user WHERE id = 0''').fetchone()[0]:
            old_smoke_variant = cur.execute('''SELECT smoke_variant FROM table_user WHERE id = 0''').fetchone()[0]
        cur.execute('''UPDATE table_user
                    SET name = ?, age = ?, smoke_variant = ?, cigarettes_per_day = ?, cigarette_cost = ?,
                    cigarette_count = ?, customs_per_day = ?, tobacco_cost = ?, tobacco_count = ?, paper_cost = ?,
                    paper_count = ?, filter_cost = ?, filter_count = ?, stics_per_day = ?, stic_cost = ?,
                    stic_count = ?, puffs_per_day = ?, vape_variant = ?, onepod_cost = ?, onepod_count = ?,
                    liquid_cost = ?, liquid_count = ?, photo_path = ?
                    WHERE id = 0
                    ''',
                    (self.name, self.age, self.smoke_variant, self.cigarettes_per_day, self.cigarette_cost,
                     self.cigarette_count, self.customs_per_day, self.tobacco_cost, self.tobacco_count, self.paper_cost,
                     self.paper_count, self.filter_cost, self.filter_count, self.stics_per_day, self.stic_cost,
                     self.stic_count, self.puffs_per_day, self.vape_variant, self.onepod_cost, self.onepod_count,
                     self.liquid_cost, self.liquid_count, self.photo_path))
        first_value, second_value = 0, 0
        if self.smoke_variant == 'Сигареты':
            first_value = self.cigarettes_per_day
            if self.cigarette_count != 0:
                second_value = self.cigarette_cost / self.cigarette_count * self.cigarettes_per_day
        elif self.smoke_variant == 'Самодельные сигареты (самокрутки)':
            first_value = self.customs_per_day
            if self.tobacco_count != 0:
                second_value += self.tobacco_cost / self.tobacco_count * 0.5 * self.customs_per_day
            if self.paper_count != 0:
                second_value += self.paper_cost / self.paper_count * self.customs_per_day
            if self.filter_count != 0:
                second_value += self.filter_cost / self.filter_count * self.customs_per_day
        elif self.smoke_variant == 'Системы нагревания табака (СНТ)':
            first_value = self.stics_per_day
            if self.stics_count != 0:
                second_value = self.stic_cost / self.stic_count * self.stics_per_day
        elif self.smoke_variant == 'Электронные сигареты':
            first_value = self.puffs_per_day
            if self.vape_variant == 'Одноразовый под':
                if self.onepod_count != 0:
                    second_value = self.onepod_cost / self.onepod_count * self.puffs_per_day
            elif self.vape_variant == 'Многоразовый под или мод':
                if self.liquid_count != 0:
                    second_value = self.liquid_cost / self.liquid_count * 0.01 * self.puffs_per_day
        if cur.execute('''SELECT * FROM table_history WHERE date = ?''',
                (datetime.strftime(datetime.today(), '%Y-%m-%d'),)).fetchone() is None:
            cur.execute('''INSERT OR IGNORE INTO table_history(date, smoked, unsmoked, spent_money, unspent_money)
                        VALUES(?, 0, ?, 0, ?)''', (datetime.strftime(datetime.today(), '%Y-%m-%d'),
                        first_value, second_value))
        if old_smoke_variant:
            smoked, unsmoked = cur.execute('''SELECT smoked, unsmoked FROM table_history WHERE date = ?''',
                                           (datetime.strftime(datetime.today(), '%Y-%m-%d'),)).fetchone()
            if old_smoke_variant == 'Электронные сигареты':
                cur.execute('''UPDATE table_statistic
                            SET value = value + ?
                            WHERE name_record = "smoked_puffs"''', (smoked,))
                cur.execute('''UPDATE table_statistic
                            SET value = value + ?
                            WHERE name_record = "unsmoked_puffs"''', (unsmoked,))
            else:
                cur.execute('''UPDATE table_statistic
                            SET value = value + ?
                            WHERE name_record = "smoked_cigarettes"''', (smoked,))
                cur.execute('''UPDATE table_statistic
                            SET value = value + ?
                            WHERE name_record = "unsmoked_cigarettes"''', (unsmoked,))
            cur.execute('''UPDATE table_history
                        SET smoked = 0, spent_money = 0
                        WHERE date = ?
                        ''',
                        (datetime.strftime(datetime.today(), '%Y-%m-%d'),))
        cur.execute('''UPDATE table_history 
                    SET unsmoked = ? - smoked, unspent_money = ? - spent_money
                    WHERE date = ?
                    ''',
                    (first_value, second_value, datetime.strftime(datetime.today(), '%Y-%m-%d')))
        self.con.commit()

        self.lk.initUI()

    def smoke(self):
        cur = self.con.cursor()
        cur.execute('''UPDATE table_history
                    SET smoked = smoked + 1
                    WHERE date = ?''', (datetime.strftime(datetime.today(), '%Y-%m-%d'),))
        cur.execute('''UPDATE table_history
                    SET unsmoked = unsmoked - 1
                    WHERE date = ?''', (datetime.strftime(datetime.today(), '%Y-%m-%d'),))
        one_cost = 0
        if self.smoke_variant == 'Сигареты':
            if self.cigarette_count != 0:
                one_cost = self.cigarette_cost / self.cigarette_count
        elif self.smoke_variant == 'Самодельные сигареты (самокрутки)':
            if self.tobacco_count != 0:
                one_cost += self.tobacco_cost / self.tobacco_count * 0.5
            if self.paper_count != 0:
                one_cost += self.paper_cost / self.paper_count
            if self.filter_count != 0:
                one_cost += self.filter_cost / self.filter_count
        elif self.smoke_variant == 'Системы нагревания табака (СНТ)':
            first_value = self.stics_per_day
            if self.stics_count != 0:
                one_cost = self.stic_cost / self.stic_count
        elif self.smoke_variant == 'Электронные сигареты':
            if self.vape_variant == 'Одноразовый под':
                if self.onepod_count != 0:
                    one_cost = self.onepod_cost / self.onepod_count
            elif self.vape_variant == 'Многоразовый под или мод':
                if self.liquid_count != 0:
                    one_cost = self.liquid_cost / self.liquid_count * 0.01
        cur.execute('''UPDATE table_history
                    SET spent_money = spent_money + ?
                    WHERE date = ?''', (one_cost, datetime.strftime(datetime.today(), '%Y-%m-%d')))
        cur.execute('''UPDATE table_history
                    SET unspent_money = unspent_money - ?
                    WHERE date = ?''', (one_cost, datetime.strftime(datetime.today(), '%Y-%m-%d')))
        self.con.commit()

        self.smoked_lcd.display(cur.execute('''SELECT smoked FROM table_history
                                            WHERE date = ?''',
                                            (datetime.strftime(datetime.today(), '%Y-%m-%d'),)).fetchall()[0][0])
        
        self.lk.initUI()

    def spend(self):
        cur = self.con.cursor()
        cur.execute('''UPDATE table_history
                    SET spent_money = spent_money + ?
                    WHERE date = ?''', (self.sum_doublespinbox.value(),
                                        datetime.strftime(datetime.today(), '%Y-%m-%d')))
        cur.execute('''UPDATE table_history
                    SET unspent_money = unspent_money - ?
                    WHERE date = ?''', (self.sum_doublespinbox.value(),
                                        datetime.strftime(datetime.today(), '%Y-%m-%d')))
        self.con.commit()

        self.sum_doublespinbox.setValue(0)

        self.lk.initUI()

    def check_date(self):
        cur = self.con.cursor()
        if cur.execute('''SELECT * FROM table_history WHERE date = ?''',
                (datetime.strftime(datetime.today(), '%Y-%m-%d'),)).fetchone():
            return
        first_value, second_value = 0, 0
        if self.smoke_variant == 'Сигареты':
            first_value = self.cigarettes_per_day
            if self.cigarette_count != 0:
                second_value = self.cigarette_cost / self.cigarette_count * self.cigarettes_per_day
        elif self.smoke_variant == 'Самодельные сигареты (самокрутки)':
            first_value = self.customs_per_day
            if self.tobacco_count != 0:
                second_value += self.tobacco_cost / self.tobacco_count * 0.5 * self.customs_per_day
            if self.paper_count != 0:
                second_value += self.paper_cost / self.paper_count * self.customs_per_day
            if self.filter_count != 0:
                second_value += self.filter_cost / self.filter_count * self.customs_per_day
        elif self.smoke_variant == 'Системы нагревания табака (СНТ)':
            first_value = self.stics_per_day
            if self.stics_count != 0:
                second_value = self.stic_cost / self.stic_count * self.stics_per_day
        elif self.smoke_variant == 'Электронные сигареты':
            first_value = self.puffs_per_day
            if self.vape_variant == 'Одноразовый под':
                if self.onepod_count != 0:
                    second_value = self.onepod_cost / self.onepod_count * self.puffs_per_day
            elif self.vape_variant == 'Многоразовый под или мод':
                if self.liquid_count != 0:
                    second_value = self.liquid_cost / self.liquid_count * 0.01 * self.puffs_per_day
        cur.execute('''INSERT OR IGNORE INTO table_history(date, smoked, unsmoked, spent_money, unspent_money)
                    VALUES(?, 0, ?, 0, ?)''', (datetime.strftime(datetime.today(), '%Y-%m-%d'),
                                               first_value, second_value))
        last_update_date = cur.execute('''SELECT value
                                       FROM table_statistic
                                       WHERE name_record = "last_updated_date"''').fetchone()[0]
        if 0 < last_update_date < int(datetime.strftime(datetime.today(), '%Y%m%d')):
            smoked, unsmoked, spent_money, unspent_money = cur.execute('''
                SELECT smoked, unsmoked, spent_money, unspent_money
                FROM table_history
                WHERE date < ?
                ORDER BY date DESC LIMIT 1
                ''',
                (datetime.strftime(datetime.today(), '%Y-%m-%d'),)).fetchone()
            cur.execute('''UPDATE table_statistic
                        SET value = ?
                        WHERE name_record = "last_updated_date"
                        ''',
                        (int(datetime.strftime(datetime.today(), '%Y%m%d')),))
            if self.smoke_variant == 'Электронные сигареты':
                smoked_variant, unsmoked_variant = 'smoked_puffs', 'unsmoked_puffs'
            else:
                smoked_variant, unsmoked_variant = 'smoked_cigarettes', 'unsmoked_cigarettes'
            cur.execute('''UPDATE table_statistic
                        SET value = value + ?
                        WHERE name_record = ?''', (smoked, smoked_variant))
            cur.execute('''UPDATE table_statistic
                        SET value = value + ?
                        WHERE name_record = ?''', (unsmoked, unsmoked_variant))
            cur.execute('''UPDATE table_statistic
                        SET value = value + ?
                        WHERE name_record = "spent_money"''', (spent_money,))
            cur.execute('''UPDATE table_statistic
                        SET value = value + ?
                        WHERE name_record = "unspent_money"''', (unspent_money,))
            cur.execute('''UPDATE table_statistic
                        SET value = ?
                        WHERE name_record = "progress"''', (unsmoked,))
        elif last_update_date == 0:
            cur.execute('''UPDATE table_statistic
                        SET value = ?
                        WHERE name_record = "last_updated_date"
                        ''',
                        (int(datetime.strftime(datetime.today(), '%Y%m%d')),))
        self.con.commit()

    '''!!!!!!!!!!'''
    def change_theme(self):
        cur = self.con.cursor()
        if self.theme == 0:
            self.theme = 1
            #self.setStyleSheet(main_style_light)
            #self.settings.setStyleSheet(settings_style_light)
            #self.lk.setStyleSheet(lk_style_light)
            #self.register.setStyleSheet(register_style_light)
            cur.execute('''UPDATE table_settings
                        SET value = 1
                        WHERE name_set = "theme"''')
        else:
            self.theme = 0
            #self.setStyleSheet(main_style_dark)
            #self.settings.setStyleSheet(settings_style_dark)
            #self.lk.setStyleSheet(lk_style_dark)
            #self.register.setStyleSheet(register_style_dark)
            cur.execute('''UPDATE table_settings
                        SET value = 0
                        WHERE name_set = "theme"''')
        self.con.commit()

    def reset(self):
        cur = self.con.cursor()
        cur.execute('''DELETE FROM table_history''')
        cur.execute('''UPDATE table_statistic
                    SET value = 0''')
        self.con.commit()

        self.initUI()
        self.lk.initUI()

    def get_statistic(self):
        cur = self.con.cursor()
        statistic = cur.execute('''SELECT * FROM table_statistic''').fetchall()
        res = []
        for row in statistic:
            if row[0] in self.active_statistics:
                res.append(row)
        return res

    def get_history(self):
        cur = self.con.cursor()
        res = cur.execute('''SELECT * FROM table_history ORDER BY DATE LIMIT 7''').fetchall()
        return res

    def change_statistic(self, m):
        cur = self.con.cursor()
        for statistic in m:
            cur.execute('''UPDATE table_settings SET value = ? WHERE name_set = ?''', (int(statistic[1]), statistic[0]))
        self.con.commit()
        self.active_statistics = [e[0] for e in cur.execute('''SELECT name_set FROM table_settings
                                                            WHERE name_set != "theme" AND value = 1''').fetchall()]
        self.lk.initUI()


#---Окно регистрации---
class Register(QWidget):
    def __init__(self, main_window):
        super().__init__()

        f = io.StringIO(register_template)
        uic.loadUi(f, self)

        self.main_window = main_window

        self.initUI()

    '''!!!!!!!!!!'''
    def initUI(self):
        #-Заполнение формы сохраненными в БД значениями-
        self.name_lineedit.setText(self.main_window.name)
        self.age_spinbox.setValue(self.main_window.age)
        self.smoke_variant_combobox.setCurrentText(self.main_window.smoke_variant)
        self.cigarettes_per_day_spinbox.setValue(self.main_window.cigarettes_per_day)
        self.cigarette_cost_doublespinbox.setValue(self.main_window.cigarette_cost)
        self.cigarette_count_spinbox.setValue(self.main_window.cigarette_count)
        self.customs_per_day_spinbox.setValue(self.main_window.customs_per_day)
        self.tobacco_cost_doublespinbox.setValue(self.main_window.tobacco_cost)
        self.tobacco_count_spinbox.setValue(self.main_window.tobacco_count)
        self.paper_cost_doublespinbox.setValue(self.main_window.paper_cost)
        self.paper_count_spinbox.setValue(self.main_window.paper_count)
        self.filter_cost_doublespinbox.setValue(self.main_window.filter_cost)
        self.filter_count_spinbox.setValue(self.main_window.filter_count)
        self.stics_per_day_spinbox.setValue(self.main_window.stics_per_day)
        self.stic_cost_doublespinbox.setValue(self.main_window.stic_cost)
        self.stic_count_spinbox.setValue(self.main_window.stic_count)
        self.puffs_per_day_spinbox.setValue(self.main_window.puffs_per_day)
        self.vape_variant_combobox.setCurrentText(self.main_window.vape_variant)
        self.onepod_cost_doublespinbox.setValue(self.main_window.onepod_cost)
        self.onepod_count_spinbox.setValue(self.main_window.onepod_count)
        self.liquid_cost_doublespinbox.setValue(self.main_window.liquid_cost)
        self.liquid_count_doublespinbox.setValue(self.main_window.liquid_count)

        #При сборке приложения переуказать путь
        if self.main_window.photo_path != 'd:\VS Code\You Can\images\default_photo.png':
            self.is_photo_loaded_label.setText('Загружено')

        self.change_smoke_variant()

        #-Подключение функций к кнопкам-
        self.smoke_variant_combobox.currentTextChanged.connect(self.change_smoke_variant)
        self.vape_variant_combobox.currentTextChanged.connect(self.change_vape_variant)
        self.load_photo_btn.clicked.connect(self.load_photo)
        self.finish_btn.clicked.connect(self.finish_registration)
        #self.setStyleSheet(register_style_dark)

    def change_smoke_variant(self):
        variant = self.smoke_variant_combobox.currentText()
        if variant == 'Сигареты':
            self.cigarette_widget.setVisible(True)
            self.custom_widget.setVisible(False)
            self.stic_widget.setVisible(False)
            self.vape_widget.setVisible(False)
            self.resize(444, 278)
        elif variant == 'Самодельные сигареты (самокрутки)':
            self.cigarette_widget.setVisible(False)
            self.custom_widget.setVisible(True)
            self.stic_widget.setVisible(False)
            self.vape_widget.setVisible(False)
            self.resize(444, 425)
        elif variant == 'Системы нагревания табака (СНТ)':
            self.cigarette_widget.setVisible(False)
            self.custom_widget.setVisible(False)
            self.stic_widget.setVisible(True)
            self.vape_widget.setVisible(False)
            self.resize(444, 278)
        elif variant == 'Электронные сигареты':
            self.cigarette_widget.setVisible(False)
            self.custom_widget.setVisible(False)
            self.stic_widget.setVisible(False)
            self.vape_widget.setVisible(True)
            self.vape1_widget.setVisible(True)
            self.vape2_widget.setVisible(False)
            self.resize(444, 305)

    def change_vape_variant(self):
        variant = self.vape_variant_combobox.currentText()
        if variant == 'Одноразовый под':
            self.vape1_widget.setVisible(True)
            self.vape2_widget.setVisible(False)
        elif variant == 'Многоразовый под или мод':
            self.vape1_widget.setVisible(False)
            self.vape2_widget.setVisible(True)

    def load_photo(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Выбрать фото профиля', '','Фото (*.jpg *.png);;Все файлы (*)')
        if not fname:
            return

        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
        else:
            app_dir = os.path.dirname(os.path.abspath(__file__))
        images_dir = os.path.join(app_dir, "images")
        if not os.path.exists(images_dir):
            os.makedirs(images_dir)
        
        pixmap = QPixmap(fname)
        side = min(pixmap.width(), pixmap.height())
        x = (pixmap.width() - side) // 2
        y = (pixmap.height() - side) // 2
        new_pixmap = pixmap.copy(x, y, side, side)

        new_path = os.path.join(images_dir, f"photo.png")
        success = new_pixmap.save(new_path, "PNG")
        if not success:
            QMessageBox.warning(self, "Ошибка", "Не удалось сохранить фото.")
            return
        self.main_window.photo_path = new_path
        self.is_photo_loaded_label.setText('Загружено')

    def finish_registration(self):
        #-Проверка заполнения обязательных полей-
        message_error = []
        if not self.name_lineedit.text():
            message_error.append('имя')
        if not self.age_spinbox.value():
            message_error.append('возраст')
        variant = self.smoke_variant_combobox.currentText()
        if variant == 'Сигареты':
            if self.cigarettes_per_day_spinbox.value() == 0:
                message_error.append('сколько вы курите в день')
            if self.cigarette_cost_doublespinbox.value() != 0 and self.cigarette_count_spinbox.value() == 0:
                message_error.append('сколько сигарет в одной пачке')
        elif variant == 'Самодельные сигареты (самокрутки)':
            if self.customs_per_day_spinbox.value() == 0:
                message_error.append('сколько вы курите в день')
            if self.tobacco_cost_doublespinbox.value() != 0 and self.tobacco_count_spinbox.value() == 0:
                message_error.append('сколько грамм табака в одном кисете')
            if self.paper_cost_doublespinbox.value() != 0 and self.paper_count_spinbox.value() == 0:
                message_error.append('сколько бумаги для самокруток в одной пачке')
            if self.filter_cost_doublespinbox.value() != 0 and self.filter_count_spinbox.value() == 0:
                message_error.append('сколько фильтров/типок в одной пачке')
        elif variant == 'Системы нагревания табака (СНТ)':
            if self.stics_per_day_spinbox.value() == 0:
                message_error.append('сколько вы курите в день')
            if self.stic_cost_doublespinbox.value() != 0 and self.stic_count_spinbox.value() == 0:
                message_error.append('сколько стиков в одной пачке')
        elif variant == 'Электронные сигареты':
            if self.puffs_per_day_spinbox.value() == 0:
                message_error.append('сколько вы курите в день')
            variant2 = self.vape_variant_combobox.currentText()
            if variant2 == 'Одноразовый под':
                if self.onepod_cost_doublespinbox.value() != 0 and self.onepod_count_spinbox.value() == 0:
                    message_error.append('на сколько затяжек рассчитан один под')
            elif variant2 == 'Многоразовый под или мод':
                if self.liquid_cost_doublespinbox.value() != 0 and self.liquid_count_doublespinbox.value() == 0:
                    message_error.append('сколько жидкости в одном флаконе')
        if message_error:
            message_error = ', '.join(message_error)
            QMessageBox.warning(self, 'Ошибка регистрации', f'Вы не заполнили поля: {message_error}.')
            return

        #-Запись значений в переменные main_window-
        self.main_window.name = self.name_lineedit.text()
        self.main_window.age = int(self.age_spinbox.value())
        self.main_window.smoke_variant = self.smoke_variant_combobox.currentText()
        if self.main_window.smoke_variant == 'Сигареты':
            self.main_window.cigarettes_per_day = self.cigarettes_per_day_spinbox.value()
            self.main_window.cigarette_cost = self.cigarette_cost_doublespinbox.value()
            self.main_window.cigarette_count = self.cigarette_count_spinbox.value()
        elif self.main_window.smoke_variant == 'Самодельные сигареты (самокрутки)':
            self.main_window.customs_per_day = self.customs_per_day_spinbox.value()
            self.main_window.tobacco_cost = self.tobacco_cost_doublespinbox.value()
            self.main_window.tobacco_count = self.tobacco_count_spinbox.value()
            self.main_window.paper_cost = self.paper_cost_doublespinbox.value()
            self.main_window.paper_count = self.paper_count_spinbox.value()
            self.main_window.filter_cost = self.filter_cost_doublespinbox.value()
            self.main_window.filter_count = self.filter_count_spinbox.value()
        elif self.main_window.smoke_variant == 'Системы нагревания табака (СНТ)':
            self.main_window.stics_per_day = self.stics_per_day_spinbox.value()
            self.main_window.stic_cost = self.stic_cost_doublespinbox.value()
            self.main_window.stic_count = self.stic_count_spinbox.value()
        elif self.main_window.smoke_variant == 'Электронные сигареты':
            self.main_window.puffs_per_day = self.puffs_per_day_spinbox.value()
            self.main_window.vape_variant = self.vape_variant_combobox.currentText()
            if self.main_window.vape_variant == 'Одноразовый под':
                self.main_window.onepod_cost = self.onepod_cost_doublespinbox.value()
                self.main_window.onepod_count = self.onepod_count_spinbox.value()
            elif self.main_window.vape_variant == 'Многоразовый под или мод':
                self.main_window.liquid_cost = self.liquid_cost_doublespinbox.value()
                self.main_window.liquid_count = self.liquid_count_doublespinbox.value()
        self.main_window.set_settings()
        self.main_window.show()
        self.close()


#---Окно настроек---
class Settings(QWidget):
    def __init__(self, main_window):
        super().__init__()

        f = io.StringIO(settings_template)
        uic.loadUi(f, self)

        self.main_window = main_window

        self.initUI()

    '''!!!!!!!!!!'''
    def initUI(self):
        self.checkboxes = [
            (self.smoked_cigarettes_checkbox, 'smoked_cigarettes'),
            (self.unsmoked_cigarettes_checkbox, 'unsmoked_cigarettes'),
            (self.smoked_puffs_checkbox, 'smoked_puffs'),
            (self.unsmoked_puffs_checkbox, 'unsmoked_puffs'),
            (self.spent_checkbox, 'spent_money'),
            (self.unspent_checkbox, 'unspent_money'),
            (self.progress_checkbox, 'progress')
        ]
        for checkbox in self.checkboxes:
            if checkbox[1] in self.main_window.active_statistics:
                checkbox[0].setChecked(True)
            else:
                checkbox[0].setChecked(False)

        self.change_data_btn.clicked.connect(self.main_window.register.show)
        self.change_theme_btn.clicked.connect(self.change_theme)
        self.reset_btn.clicked.connect(self.reset)
        self.smoked_cigarettes_checkbox.stateChanged.connect(self.change_statistic)
        self.unsmoked_cigarettes_checkbox.stateChanged.connect(self.change_statistic)
        self.smoked_puffs_checkbox.stateChanged.connect(self.change_statistic)
        self.unsmoked_puffs_checkbox.stateChanged.connect(self.change_statistic)
        self.spent_checkbox.stateChanged.connect(self.change_statistic)
        self.unspent_checkbox.stateChanged.connect(self.change_statistic)
        self.progress_checkbox.stateChanged.connect(self.change_statistic)
        #self.setStyleSheet(settings_style_dark)

    '''!!!!!!!!!!'''
    def change_theme(self):
        if self.change_theme_btn.text() == 'Светлая тема':
            self.change_theme_btn.setText('Темная тема')
        else:
            self.change_theme_btn.setText('Светлая тема')
        #self.main_window.change_theme()

    def change_statistic(self):
        res = []
        for checkbox in self.checkboxes:
            res.append((checkbox[1], checkbox[0].isChecked()))
        self.main_window.change_statistic(res)

    def reset(self):
        question = QMessageBox.question(
            None,
            'Подтверждение',
            'Вы уверены, что хотите безвозвратно очистить статистику и историю?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if question == QMessageBox.StandardButton.No:
            return
        self.main_window.reset()


#---Окно личного кабинета---
class Lk(QWidget):
    def __init__(self, main_window):
        super().__init__()

        f = io.StringIO(lk_template)
        uic.loadUi(f, self)

        self.main_window = main_window

        self.initUI()

    '''!!!!!!!!!!'''
    def initUI(self):
        self.pixmap = QPixmap(self.main_window.photo_path)
        self.photo_label.setPixmap(self.pixmap.scaled(self.photo_label.width(), self.photo_label.height(),
                                   Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        self.name_label.setText(self.main_window.name)
        self.age_label.setText(str(self.main_window.age) + ' лет')

        self.statistic_tablewidget.setRowCount(0)
        rows = self.main_window.get_statistic()
        self.statistic_tablewidget.setRowCount(len(rows))
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                if isinstance(val, float):
                    val = f'{val:.2f}'
                item = QTableWidgetItem(str(val))
                self.statistic_tablewidget.setItem(r, c, item)
        self.statistic_tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.history_tablewidget.setRowCount(0)
        rows = self.main_window.get_history()
        self.history_tablewidget.setRowCount(len(rows))
        
        for r, row in enumerate(rows):
            for c, val in enumerate(row):
                if isinstance(val, float):
                    val = f'{val:.2f}'
                item = QTableWidgetItem(str(val))
                self.history_tablewidget.setItem(r, c, item)
        self.history_tablewidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.statistic_csv_btn.clicked.connect(self.statistic_csv)
        self.statistic_txt_btn.clicked.connect(self.statistic_txt)
        self.history_csv_btn.clicked.connect(self.history_csv)
        self.history_txt_btn.clicked.connect(self.history_txt)

        #self.setStyleSheet(lk_style_dark)

    def statistic_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как", "", "CSV file (*.csv)"
        )
        if not path:
            return
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            headers = [self.statistic_tablewidget.horizontalHeaderItem(i).text()
                       for i in range(self.statistic_tablewidget.columnCount())]
            writer.writerow(headers)
            for r in range(self.statistic_tablewidget.rowCount()):
                row = []
                for c in range(self.statistic_tablewidget.columnCount()):
                    it = self.statistic_tablewidget.item(r, c)
                    row.append("" if it is None else it.text())
                writer.writerow(row)

    def statistic_txt(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как", "", "TXT file (*.txt)"
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            headers = [self.statistic_tablewidget.horizontalHeaderItem(i).text()
                       for i in range(self.statistic_tablewidget.columnCount())]
            f.write(', '.join(headers) + '\n')
            for r in range(self.statistic_tablewidget.rowCount()):
                row = []
                for c in range(self.statistic_tablewidget.columnCount()):
                    it = self.statistic_tablewidget.item(r, c)
                    row.append("" if it is None else it.text())
                f.write(', '.join(row) + '\n')

    def history_csv(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как", "", "CSV file (*.csv)"
        )
        if not path:
            return
        with open(path, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            headers = [self.history_tablewidget.horizontalHeaderItem(i).text()
                       for i in range(self.history_tablewidget.columnCount())]
            writer.writerow(headers)
            for r in range(self.history_tablewidget.rowCount()):
                row = []
                for c in range(self.history_tablewidget.columnCount()):
                    it = self.history_tablewidget.item(r, c)
                    row.append("" if it is None else it.text())
                writer.writerow(row)

    def history_txt(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Сохранить как", "", "TXT file (*.txt)"
        )
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            headers = [self.history_tablewidget.horizontalHeaderItem(i).text()
                       for i in range(self.history_tablewidget.columnCount())]
            f.write(', '.join(headers) + '\n')
            for r in range(self.history_tablewidget.rowCount()):
                row = []
                for c in range(self.history_tablewidget.columnCount()):
                    it = self.history_tablewidget.item(r, c)
                    row.append("" if it is None else it.text())
                f.write(', '.join(row) + '\n')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Main()
    sys.exit(app.exec())
