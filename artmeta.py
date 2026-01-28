from urllib.parse import urlparse

metadata=dict()

def is_url(url_string):
    try:
        result = urlparse(url_string)
        # Check if both scheme and network location are present and non-empty
        return all([result.scheme, result.netloc])
    except ValueError: # Handle potential parsing errors, though urlparse usually handles them gracefully
        return False

def get_url(prompt):
    while True:
        data=input("Please input the URL "+prompt+" [URL, required] ")
        if (not is_url(data)):
            print("This is not a URL. Please input a valid URL.")
        else:
            break
    return data

def get_nonblank(prompt):
    while True:
        data=input(prompt+" [text or URL, required] ")
        if data.strip() == "":
            print("This response cannot be blank.")
        else:
            break
    return data

def get_blank(prompt):
    data=input(prompt+" [text or URL, optional] ")
    return data

def get_nonblank_multi(prompt):
    while True:
        odata=""
        data=input(prompt + " [text or URL, required] ")
        while True:
            if data.strip() == "":
                break
            else:
                if odata != "":
                    odata += "\n"
                odata += data
                data=input()
        if odata.strip() == "":
            print("This response cannot be blank.")
        else:
            break
    return odata


def get_code_artifact(badge):
    if badge == 'f' or badge == 'r':
        pubpriv=input("Does your artifact use public infrastructure? [y]es or [n]o ")

        if pubpriv != "y" and pubpriv != "Y":
            pubpriv="n"
        else:
            pubpriv="y"

        if pubpriv=="y":
            metadata['infrastructure_url'] = get_url("the infrastructure you used")
            metadata['infrastructure_resources']=get_url("the file that describes infrastructure resources you used.")
            metadata['infrastructure_allocation']=get_blank("Please input any special allocation instructions.")
        else:
            metadata['infrastructure_constraints']=get_nonblank("Please input the reason for not using public infrastructure, such as special hardware that was not available.")
            metadata['infrastructure_access']=get_blank("Please input instructions for how evaluators can access your private infrastructure. If you leave this blank, evaluators will try to evaluate on their private infrastructure, but they may run into issues.")

        metadata['install_script']=get_url("your installation script.")
        metadata['use']=get_blank("Please provide any notes about intended use of your artifact and any limitations of your research artifact, i.e., what use is it NOT suitable for.")
        metadata['destructive']=get_blank("Please provide any notes about destructive actions your artifact can cause.")
        num=1
        while True:
            metadata['claim'+str(num)]=get_nonblank("Please input text of claim "+str(num))
            metadata['script'+str(num)]=get_url("the claim-running script or instructions.")
            metadata['expected'+str(num)]=get_nonblank("Describe the expected outcome that would validate the claim. This can also be a pointer to a file in your repository")
            while True:
                more=input("Do you have more claims? [y]es or [n]o ")
                more = more.lower().strip()
                if more != "y" and more != "n":
                    print("Valid respones only include [y] or [n]")
                else:
                    break
            if more == "n":
                break
            num += 1
            
    return


def get_data_artifact():
    
    survey=input("Does your artifact include only user survey instruments (without results)? [y]es or [n]o ")

    if survey!="y" and survey !="Y":
        survey="n"
    else:
        survey="y"

    if survey == "n":
        metadata['provenance']=get_url("the file (ideally in your artifact repository) that describes how data was collected, where, when the collection started and ended. Be as detailed as possible.")
        metadata['use']=get_blank("Please provide any notes about intended use of your artifact and any limitations of your data collection.")
        metadata['ethics']=get_url("the file that discusses ethics of your data collection process. This can be a copy of the ethics section from your paper.")
        
    return

while True:
    badge=input("Please specify which badges you are requesting - [a]vailable, [f]unctional or [r]esults reproduced ")
    badge = badge.lower().strip()
    if badge != "a" and badge != "f" and badge != "r":
        print("Valid responses only include [a], [f] or [r]")
    else:
        break
    
metadata['badge'] = badge
metadata['artifact_url']=get_url("your artifact, e.g., Github repo ")


while True:
    cd=input("Is your artifact [c]ode, [d]ataset or [b]oth? ")
    cd = cd.lower().strip()
    if cd != "c" and cd != "d" and cd != "b":
        print("Valid respones only include [c], [d] or [b]")
    else:
        break

metadata['cd'] = cd

metadata['citation']=get_nonblank_multi("Please input your paper's citation in bibtex format. It is OK if this is an incomplete citation, e.g., missing a DOI or page numbers. End with an empty line.")
metadata['license_url']=input("Please provide a URL for the license you plan to use to release the artifact to the public. Leave blank if none. ")

if cd == "c" or cd == "b":
    get_code_artifact(badge)

if cd == "d" or cd == "b":
    get_data_artifact()

metadata['readme']=get_url("the README file that contains any remaining instructions about your artifact, either to the AEC or for future reuse.")
metadata['hw']=get_blank("Please specify any special hw requirements for evaluators, such as CPU, GPU, memory, etc. [text, optional]")
metadata['sw']=get_blank("Please specify any special sw requirements for evaluators, such as OS, paid software packages or software that requires a non-Linux environment to run [text, optional]")
metadata['api']=get_blank("Please specify if your artifact needs API keys to access paid services online [text, optional]")
while True:
    gui=get_nonblank("Does your artifact require a GUI - [y]es or [n]o")
    gui = gui.lower().strip()
    if gui != "y" and gui != "n":
        print("Valid respones only include [y] or [n]")
    else:
        break
metadata['gui'] = gui

print("\n\n=== PLEASE COPY/PASTE THE OUTPUT BELOW INTO THE HOTCRP ===")
for m in metadata:
    print(m+":\""+metadata[m] + "\"")

