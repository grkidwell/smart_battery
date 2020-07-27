full_addr_dict = {'Volt'     :[0X09],
                 'Curr'      :[0X0A],
                 'SOC'       :[0X0D],
                 'mAhr'      :[0X0F],
                 'Temp'      :[0X08],
                 'Icharge'   :[0X14], #Charging Current
                 'Vcharge'   :[0X15], #Charging Voltage
                 'mAhrFull'  :[0X10], #Full Charge Capacity
                 'mAhrDesign':[0X18], #Design Capacity
                 'VoltDesign':[0X19], #Design Voltage
                 'ManufDate' :[0X1B], #Manufacturer Date
                 'Chemistry' :[0X22]  #Device Chemistry
                 }

scale_dict = {'Volt'      :0.001,
              'Curr'      :0.001,
              'SOC'       :1,
              'mAhr'      :1,
              'Temp'      :1,
              'Icharge'   :0.001,
              'Vcharge'   :0.001,
              'mAhrFull'  :1,
              'mAhrDesign':1,
              'VoltDesign':0.001,
              'ManufDate' :1,
              'Chemistry' :1
                 }

abrev_addr_dict = {'Volt':[0X09],
                   'Curr':[0X0A],
                   'SOC' :[0X0D],
                   'Temp':[0X08]
                   }

dell_bat_enable = { 'manufacturer access'   : [0X00],
                    'battery mode'          : [0X03]}

WRITE1  = ['Write',[0X00]]#Manufacturer Access
READ1   = ['Read' ,     1]
WRITE2  = ['Write',[0X03]]#Battery Mode
READ2   = ['Read',      2]
WRITE29 = ['Write',[0X00,0X08,0X00]]

#Minimum needed to turn on battery charge FET
cont_call = [WRITE29,WRITE1,READ2,WRITE1,READ2,WRITE2,READ2]
