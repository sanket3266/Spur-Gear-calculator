from gear import *
def userint():
  tmp = {}
  base_prompt = """
      P <Value of power in KW>
      Z1 <Number of teeth on Pinion>
      Z2 <Number of teeth on Gear>
      alpha <1 for 14.5 degree involute
              2 for 20 degrees involute
              3 for 20 degrees Stub >
      N1 <Speed of Pinion in RPM>
      N2 <Speed of Gear in RPM>
      sig1 <Allowable stress of Pinion in MPa>
      sig2 <Allowable stress of Gear in MPa>
      E2 <Young's Modulus of Gear in MPa>
      E1 <Young's Modulus of Pinion in MPa>
      Cs <Service Factor>
      Condition <1 for Iron on Iron
                  2 for Iron on Steel
                  3 for Steel on Steel>
      Quit (Quit only after all the variable below have been input)
      (If Not given give zero)
      Choice: """
  feedback = ""
  while True:
      action = input(feedback + "\n" + base_prompt)
      feedback = ""
      words = action.split()
      if len(words) > 0:
          command = words[0]
      else:
          command = None
      if command == "Quit":
          print("Exiting...")
          return tmp
      elif command == "P" and len(words) == 2:
        tmp['P']=float(words[1])
        feedback+=f'Power entered {words[1]}Kw is added'

      elif command == "Z1" and len(words) == 2:
        tmp['Z1']=float(words[1])
        feedback += f'Pinion teeth entered {words[1]}'

      elif command == "Z2" and len(words) == 2:
        tmp['Z2']=float(words[1])
        feedback += f'Gear teeth entered {words[1]} '

      elif command == "alpha" and len(words) == 2:
        tmp['alpha']=int(words[1])
        feedback += f'The option chosen for pressure angle is {words[1]}'
      elif command == "N1" and len(words) == 2:
        tmp['N1']=float(words[1])
        feedback += f'Speed of pinion entered is {words[1]}'
      elif command == "N2" and len(words) == 2:
        tmp['N2']=float(words[1])
        feedback += f'Speed of gear entered is {words[1]}'
      elif command == "sig1" and len(words) == 2:
        tmp['sig1']=float(words[1])
        feedback += f'The allovable stress for pinion entered is {words[1]}'
      elif command == "sig2" and len(words) == 2:
        tmp['sig2']=float(words[1])
        feedback += f'The allovable stress for gear entered is {words[1]}'
      elif command == "E2" and len(words) == 2:
        tmp['E2']=float(words[1])
        feedback += f'The Youngs modulas for gear entered is {words[1]}'
      elif command == "E1" and len(words) == 2:
        tmp['E1']=float(words[1])
        feedback += f'The Youngs modulas for pinion entered is {words[1]}'
      elif command == "Cs" and len(words) == 2:
        tmp['Cs']=float(words[1])
        feedback += f'Service factor entered is {words[1]}'
      elif command == 'Condition' and len(words) == 2:
        tmp['Condition'] = int(words[1])
        feedback += f'You have selected {words[1]} as the condition between gears'
      else:
          feedback+= "I didn't understand that. Please try again."

def cal():
  data = Spurgear(t['Condition'],
                    t['alpha'],
                    t['P'],
                    t['sig1'],
                    t['sig2'],
                    t['Cs'],
                    t['N1'],
                    t['N2'],
                    t['Z1'],
                    t['Z2'],
                    t['E1'],
                    t['E2'])
  base_prompt = """
      a (To determine the module)
      b (To Give the face width of the gears)
      c (To check for strength)
      d (to get Dynamic factor)
      e (to get Dynamic load)
      f (BHN of the Pinion)
      g (Dia of pinion and Gear)
      Quit/Q (Quit only after all the variable below have been input)
      Choice: """
  feedback = ""
  while True:
    action = input(feedback + '\n' + base_prompt)
    feedback = ''
    words = action.split()
    if len(words) != 0:
        command = words[0]
    else:
        command = None
    if command == 'a':
        t1 = data.module()
        feedback += f'The module for the given gears is {t1} mm'
    elif command == 'b':
        data.module()
        t1 = data.b
        feedback += f'The face width of the given gears is {t1} mm'
    elif command == 'c':
        t1 = data.check_for_stress()
        feedback+=t1
    elif command == 'd':
        t1 = data.dynamic_fac()
        feedback+= f'The dynamic load factor of the gears is {t1}'
    elif command == 'e':
        t1 = data.dynamic_load()
        feedback += f'The dynamic load of the gears is {t1}N'
    elif command == 'f':
        t1 = data.BHN()
        feedback += f'The BHN of pinion is {t1[0]} and of gear is {t1[1]}'
    elif command == 'g':
        data.module()
        t1 = [data.d1,data.d2]
        feedback += f'The diameter of pinion is {t1[0]} mm and gear is {t1[1]} mm'
    elif command == 'Quit' or command == 'q':
        return
    else:
      feedback += "I didn't understand that. Please try again."

tmp = userint()
try :
  t = {"P": tmp['P'],
        "Z1": tmp['Z1'],
        "Z2": tmp['Z2'],
        "alpha": tmp['alpha'],
        "N1": tmp['N1'],
        "N2": tmp['N2'],
       "sig1": tmp['sig1'],
        "sig2": tmp['sig2'],
        "E2": tmp['E2'],
        "E1": tmp['E1'],
        "Cs": tmp['Cs'],
        'Condition': tmp['Condition']}
  cal()
  print('Thanks for using our program')
except: 
  print("Insufficient Data")