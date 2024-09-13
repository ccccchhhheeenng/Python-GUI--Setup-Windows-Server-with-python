import tkinter as tk
import time
import threading
import subprocess
from tkinter import ttk

root = tk.Tk()
root.title('Windows Server Setup')
root.geometry('400x400')
current_interface = list()
#Style
style = ttk.Style()
style.configure('Custom.TButton', font=('Helvetica', 12), foreground='blue', padding=5)
style.configure('Red.TButton', font=('Helvetica', 12), foreground='red', padding=5)
style.configure('Green.TButton', font=('Helvetica', 12), foreground='green', padding=5)

#powershell
def powershell(command):
    subprocess.run(["powershell.exe", command])

#-----<Interface>-----
def update_interface():
    for widget in root.winfo_children():
        widget.destroy()
    if len(current_interface)==0:
        setup_main_interface()
    if "DHCP" in current_interface:
        setup_DHCP_interface()
    if "DNS" in current_interface:
        setup_DNS_interface()
    if "RemoveDHCP" in current_interface:
        Remove_DHCP_Scope_interface()
#---------------------
def back():
    current_interface.pop()
    update_interface()
def DHCP_Setup_Click():
    current_interface.append("DHCP")
    update_interface()
def DNS_Setup_click():
    current_interface.append("DNS")
    update_interface()
def Remove_DHCP_Scope_Click():
    current_interface.append("RemoveDHCP")
    update_interface()
def Add_DNS_Primary_Zone_Click():
    current_interface.append("Add_DNS_Primary_Zone")
    update_interface()
def Add_DNS_Primary_Record_Click():
    current_interface.append("Add_DNS_Primary_Record")
    update_interface()
def Remove_DNS_Primary_Zone_Click():
    current_interface.append("Remove_DNS_Primary_Zone")
    update_interface()
def Remove_DNS_Primary_Record_Click():
    current_interface.append("Remove_DNS_Primary_Record")
    update_interface()

#-----</Interface>-----

#-----</Main Interface>-----
def setup_main_interface():

#-------<Install tools>-----

    #-----<DHCP_Install>-----
    def DHCP_Install_Click():
        DHCP_install_thread = threading.Thread(target=installing_DHCP)
        DHCP_install_thread.start()
        DHCP_Install.config(text='Installing')

    def installing_DHCP():
        powershell("Install-WindowsFeature -Name 'DHCP' –IncludeManagementTools")
        DHCP_complete_thread = threading.Thread(target=Func_DHCP_complete)
        DHCP_complete_thread.start()
        DHCP_Install.config(text="Finished")  

    def Func_DHCP_complete():
        time.sleep(3)
        DHCP_Install.config(text="Install DHCP Feature")  
    #-----</DHCP_Install>-----
        
    #-----<DHCP_Uninstall>-----
    def DHCP_Uninstall_Click():
        DHCP_Uninstall_thread = threading.Thread(target=Uninstalling_DHCP)
        DHCP_Uninstall_thread.start()
        DHCP_Uninstall.config(text='Uninstalling')

    def Uninstalling_DHCP():
        powershell("Uninstall-WindowsFeature -Name 'DHCP' –IncludeManagementTools")
        DHCP_complete_thread = threading.Thread(target=Func_UnDHCP_complete)
        DHCP_complete_thread.start()

    def Func_UnDHCP_complete():
        DHCP_Uninstall.config(text="Finished")  
        time.sleep(3)
        DHCP_Uninstall.config(text="Uninstall DHCP Feature")  
    #-----</DHCP_Uninstall>-----
    
#-------</Install tools>-----

    #-----<Main Window Buttons>-----
    DHCP_Install = ttk.Button(root, text='Install DHCP Feature', command=DHCP_Install_Click, style='Custom.TButton')
    DHCP_Install.pack()
    DHCP_Uninstall = ttk.Button(root, text='Uninstall DHCP Feature', command=DHCP_Uninstall_Click, style='Custom.TButton')
    DHCP_Uninstall.pack()
    Setup_DHCP = ttk.Button(root, text="Setup DHCP", command=DHCP_Setup_Click, style='Custom.TButton')
    Setup_DHCP.pack()
    Setup_DNS=ttk.Button(root,text="Setup DNS",command=DNS_Setup_click, style='Custom.TButton')
    Setup_DNS.pack()
    Remove_DHCP_Scope=ttk.Button(root,text="Remove DHCP Scope",command=Remove_DHCP_Scope_Click, style='Custom.TButton')
    Remove_DHCP_Scope.pack()    
    #-----</Main Window Buttons>-----
#-----</Main Interface>-----

#-----<DHCP Interface>-----
def setup_DHCP_interface():
    def DHCP_Finish_Button():
        DHCP_Setup_thread = threading.Thread(target=DHCP_Finish_Button_Run)
        DHCP_Setup_thread.start()
        read_input.config(text="Please Wait")
        
    #<Get user input data>
    def DHCP_Finish_Button_Run():
        StartRange=StartRangeentry.get()
        EndRange=EndRangeentry.get()
        SubnetMask=SubnetMaskentry.get()
        ScopeName=ScopeNameentry.get()
        DNS_Address=DNS_Addressentry.get()
        Router=Routerentry.get()
        #<Scope id calculate>
        r=StartRange.split(".")
        ScopeID=""
        for i in range(3):
            ScopeID+=r[i]
            ScopeID+="."
        ScopeID+="0"
        #</Scope id calculate>
        AddScope="Add-DhcpServerV4Scope -Name "+ScopeName+" -StartRange "+StartRange+" -EndRange "+EndRange+" -Subnetmask "+SubnetMask
        powershell(AddScope)
        SetDHCPDNS="Set-DhcpServerv4OptionValue -ScopeId "+ScopeID+" -OptionId 6 -Value "+DNS_Address
        powershell(SetDHCPDNS)
        SetDHCPRouter="Set-DhcpServerv4OptionValue -ScopeId "+ScopeID+" -Router "+Router
        powershell(SetDHCPRouter)
        back()      
    StartRangelabel = tk.Label(root, text='StartRange:')
    StartRangelabel.grid(row=0, column=0)
    StartRangeentry = tk.Entry(root)
    StartRangeentry.grid(row=0, column=1)
    EndRangelabel = tk.Label(root, text='EndRange:')
    EndRangelabel.grid(row=1, column=0)
    EndRangeentry = tk.Entry(root)
    EndRangeentry.grid(row=1, column=1)
    SubnetMasklabel = tk.Label(root, text='SubnetMask:')
    SubnetMasklabel.grid(row=2, column=0)
    SubnetMaskentry = tk.Entry(root)
    SubnetMaskentry.grid(row=2, column=1)
    ScopeNamelabel = tk.Label(root, text='ScopeName:')
    ScopeNamelabel.grid(row=3, column=0)
    ScopeNameentry = tk.Entry(root)
    ScopeNameentry.grid(row=3, column=1)
    DNS_Addresslabel = tk.Label(root, text='DNS Address:')
    DNS_Addresslabel.grid(row=4, column=0)
    DNS_Addressentry = tk.Entry(root)
    DNS_Addressentry.grid(row=4, column=1)
    Routerlabel = tk.Label(root, text='Router IP:')
    Routerlabel.grid(row=5, column=0)
    Routerentry = tk.Entry(root)
    Routerentry.grid(row=5, column=1)
    Exit = ttk.Button(root, text="Exit", command=back, style='Red.TButton')
    Exit.grid(row=6, column=0, padx=20)
    read_input=ttk.Button(root, text="Finish", command=DHCP_Finish_Button, style='Green.TButton')
    read_input.grid(row=6,column=1)
#-----</DHCP Interface>-----


def Remove_DHCP_Scope_interface():
    def DHCP_Finish_Button():
        DHCP_Setup_Thread=threading.Thread(target=DHCP_Finish_Button_Run)
        read_input.config(text="Please Wait")
        DHCP_Setup_Thread.start()
    def DHCP_Finish_Button_Run():
        ScopeID=ScopeIDentry.get()
        command="Remove-DhcpServerv4Scope -ScopeId "+ScopeID
        powershell(command)
        back()

    ScopeIDlabel = tk.Label(root, text='ScopeID:')
    ScopeIDlabel.grid(row=0, column=0)
    ScopeIDentry = tk.Entry(root)
    ScopeIDentry.grid(row=0, column=1)
    Exit=ttk.Button(root, text="Exit", command=back, style='Red.TButton')
    Exit.grid(row=6,column=0,padx=20)
    read_input=ttk.Button(root, text="Finish", command=DHCP_Finish_Button, style='Green.TButton')
    read_input.grid(row=6,column=1) 
def setup_DNS_interface():
    if "Foward_Lookup_Zone" in current_interface:
        if "Add_DNS_Primary_Zone" in current_interface:
            def Add_Primary_Zone_Click():
                DNS_install_thread = threading.Thread(target=Adding_Zone)
                DNS_install_thread.start()
                Add_Primart_Zone_input.config(text="Please Wait")
            def Adding_Zone():
                ZoneName=ZoneNameEntry.get()
                ZoneFile=ZoneName+".dns"
                command="Add-DnsServerPrimaryZone -Name "+ZoneName+" -ZoneFile "+ZoneFile
                powershell(command)
                back()
            ZoneNamelabel=tk.Label(root,text="Zone Name")
            ZoneNamelabel.grid(row=0,column=0)
            ZoneNameEntry=tk.Entry(root)
            ZoneNameEntry.grid(row=0,column=1)
            Exit=ttk.Button(root,text="Exit",command=back, style='Red.TButton')
            Exit.grid(row=1,column=0,padx=20)
            Add_Primart_Zone_input=ttk.Button(root,text="Finish",command=Add_Primary_Zone_Click, style='Green.TButton')
            Add_Primart_Zone_input.grid(row=1,column=1)
        elif "Add_DNS_Primary_Record" in current_interface:
            def DNS_Record_input_Click():
                tmp=Set_Record_Type.get()
                for widget in root.winfo_children():
                    widget.destroy()
                if tmp=="A":
                    def A_input_Click():
                        DNS_install_thread = threading.Thread(target=installing_DNS_A)
                        DNS_install_thread.start()
                        A_input.config(text="Please Wait")
                    def installing_DNS_A():
                        zone=Set_Zone_Entry.get()
                        name=Name_Entry.get()
                        IPv4Address=IPv4Address_Entry.get()
                        command="Add-DnsServerResourceRecordA -Name "+name+" -ZoneName "+zone+" -IPv4Address "+IPv4Address
                        powershell(command)
                        update_interface()
                    Name_Label=tk.Label(root,text="Name:")
                    Name_Label.grid(row=0,column=0)
                    Name_Entry=tk.Entry(root)
                    Name_Entry.grid(row=0,column=1)
                    IPv4Address_Label=tk.Label(root,text="IPv4Address:")
                    IPv4Address_Label.grid(row=1,column=0)
                    IPv4Address_Entry=tk.Entry(root)
                    IPv4Address_Entry.grid(row=1,column=1)
                    Exit=ttk.Button(root,text="Back",command=update_interface, style='Red.TButton')
                    Exit.grid(row=2,column=0,padx=20)
                    A_input=ttk.Button(root,text="Finish",command=A_input_Click, style='Green.TButton')
                    A_input.grid(row=2,column=1)
                elif tmp=="AAAA":
                    def AAAA_input_Click():
                        DNS_install_thread = threading.Thread(target=installing_DNS_AAAA)
                        DNS_install_thread.start()
                        AAAA_input.config(text="Please Wait")
                    def installing_DNS_AAAA():
                        zone=Set_Zone_Entry.get()
                        name=Name_Entry.get()
                        IPv6Address=IPv6Address_Entry.get()
                        command="Add-DnsServerResourceRecordAAAA -Name "+name+" -ZoneName "+zone+" -IPv6Address "+IPv6Address
                        powershell(command)
                        update_interface()
                    Name_Label=tk.Label(root,text="Name:")
                    Name_Label.grid(row=0,column=0)
                    Name_Entry=tk.Entry(root)
                    Name_Entry.grid(row=0,column=1)
                    IPv6Address_Label=tk.Label(root,text="IPv6Address:")
                    IPv6Address_Label.grid(row=1,column=0)
                    IPv6Address_Entry=tk.Entry(root)
                    IPv6Address_Entry.grid(row=1,column=1)
                    Exit=ttk.Button(root,text="Back",command=update_interface, style='Red.TButton')
                    Exit.grid(row=2,column=0,padx=20)
                    AAAA_input=ttk.Button(root,text="Finish",command=AAAA_input_Click, style='Green.TButton')
                    AAAA_input.grid(row=2,column=1)
                else:
                    def CName_input_Click():
                        DNS_install_thread = threading.Thread(target=installing_DNS_CName)
                        DNS_install_thread.start()
                        CName_input.config(text="Please Wait")
                    def installing_DNS_CName():
                        zone=Set_Zone_Entry.get()
                        name=Name_Entry.get()
                        HostNameAlias=HostNameAlias_Entry.get()
                        command="Add-DnsServerResourceRecordCName -Name "+name+" -ZoneName "+zone+" -HostNameAlias "+HostNameAlias
                        powershell(command)
                        update_interface()
                    Name_Label=tk.Label(root,text="Name:")
                    Name_Label.grid(row=0,column=0)
                    Name_Entry=tk.Entry(root)
                    Name_Entry.grid(row=0,column=1)
                    HostNameAlias_Label=tk.Label(root,text="HostNameAlias:")
                    HostNameAlias_Label.grid(row=1,column=0)
                    HostNameAlias_Entry=tk.Entry(root)
                    HostNameAlias_Entry.grid(row=1,column=1)
                    Exit=ttk.Button(root,text="Back",command=update_interface, style='Red.TButton')
                    Exit.grid(row=2,column=0,padx=20)
                    CName_input=ttk.Button(root,text="Finish",command=CName_input_Click, style='Green.TButton')
                    CName_input.grid(row=2,column=1)
            Set_Zone_Label=tk.Label(root,text="Set Zone:")
            Set_Zone_Label.grid(row=0,column=0,)
            Set_Zone_Entry=tk.Entry(root)
            Set_Zone_Entry.grid(row=0,column=1)
            #---<!!!!!!!需合併column!!!!!>---
            Set_Record_Type_Label = ttk.Label(root, text="Record Type:")
            Set_Record_Type_Label.grid(row=1, column=0)
            Set_Record_Type=ttk.Combobox(root,values=["A","AAAA","CName"])
            Set_Record_Type.grid(row=1, column=1)
            Exit=ttk.Button(root,text="Exit",command=back, style='Red.TButton')
            Exit.grid(row=2,column=0,padx=20)
            DNS_Record_input=ttk.Button(root,text="Next",command=DNS_Record_input_Click, style='Green.TButton')
            DNS_Record_input.grid(row=2,column=1)
        elif "Remove_DNS_Primary_Zone" in current_interface:
            def DNS_Finish_Button():
                DNS_Remove_thread=threading.Thread(target=Remove_Start)
                DNS_Remove_thread.start()
                read_input.config(text="Please Wait")
            def Remove_Start():
                Zone=ZoneNameentry.get()
                command="Remove-DnsServerZone -Name "+Zone+" -Force"
                powershell(command)
                back()               
            ZoneNamelabel = tk.Label(root, text='ZoneName:')
            ZoneNamelabel.grid(row=0, column=0)
            ZoneNameentry = tk.Entry(root)
            ZoneNameentry.grid(row=0, column=1)
            Exit=ttk.Button(root, text="Exit", command=back, style='Red.TButton')
            Exit.grid(row=6,column=0,padx=20)
            read_input=ttk.Button(root, text="Finish", command=DNS_Finish_Button, style='Green.TButton')
            read_input.grid(row=6,column=1)  
        elif "Remove_DNS_Primary_Record" in current_interface:
            def DNS_Finish_Button():
                DNS_Remove_thread=threading.Thread(target=Remove_Start)
                DNS_Remove_thread.start()
                read_input.config(text="Please Wait")
            def Remove_Start():
                Zone=ZoneNameentry.get()
                Record=RecordNameentry.get()
                type=str(Set_Record_Type.get())
                command="Remove-DnsServerResourceRecord -ZoneName "+Zone+" -Name "+Record+" -RRType "+type+" -Force"
                powershell(command)
                back()
            ZoneNamelabel = tk.Label(root, text='ScopeID:')
            ZoneNamelabel.grid(row=0, column=0)
            ZoneNameentry = tk.Entry(root)
            ZoneNameentry.grid(row=0, column=1)
            RecordNamelabel = tk.Label(root, text='RecordName:')
            RecordNamelabel.grid(row=1, column=0)
            RecordNameentry = tk.Entry(root)
            RecordNameentry.grid(row=1, column=1)
            Set_Record_Type_label=tk.Label(root,text="Type")
            Set_Record_Type_label.grid(row=2,column=0)
            Set_Record_Type=ttk.Combobox(root,values=["A","AAAA","CName"])
            Set_Record_Type.grid(row=2,column=1)
            Exit=ttk.Button(root, text="Exit", command=back, style='Red.TButton')
            Exit.grid(row=6,column=0,padx=20)
            read_input=ttk.Button(root, text="Finish", command=DNS_Finish_Button, style='Green.TButton')
            read_input.grid(row=6,column=1)    
        else:
            Add_Primary_Zone_Button=ttk.Button(root,text="Add Primary Zone",command=Add_DNS_Primary_Zone_Click, style='Custom.TButton')
            Add_Primary_Zone_Button.pack()           
            Add_DNS_Record_Button=ttk.Button(root,text="Add DNS Record",command=Add_DNS_Primary_Record_Click, style='Custom.TButton')
            Add_DNS_Record_Button.pack()
            Remove_DNS_Zone_Button=ttk.Button(root,text="Remove DNS Zone",command=Remove_DNS_Primary_Zone_Click, style='Custom.TButton')
            Remove_DNS_Zone_Button.pack()
            Remove_DNS_Record_Button=ttk.Button(root,text="Remove DNS Recoed",command=Remove_DNS_Primary_Record_Click, style='Custom.TButton')
            Remove_DNS_Record_Button.pack()
            Exit=ttk.Button(root,text="Back",command=back, style='Red.TButton')
            Exit.pack() 
    else:
        def Foward_Lookup_Zone_Click():
            current_interface.append("Foward_Lookup_Zone")
            update_interface()
        Foward_Lookup_Zone=ttk.Button(root,text="Foward Look Zone Settings",command=Foward_Lookup_Zone_Click, style='Custom.TButton')
        Foward_Lookup_Zone.pack()
        Exit=ttk.Button(root,text="Back",command=back, style='Red.TButton')
        Exit.pack() 
        # Reverse_Lookup_Zone=ttk.Button(root,text="Reverse Look Zone Settings",command=Reverse_Lookup_Zone_Click, style='Custom.TButton')
        # Reverse_Lookup_Zone.pack()
        # Set_Fowarder=ttk.Button(root,text="Set Fowarder",command=Set_Fowarder_Click, style='Custom.TButton')
        # Set_Fowarder.pack()


setup_main_interface()
root.mainloop()
