3 Basic Concepts of IoT Security
Identity, Authentication, Authorization

PART 1 - Identify security vulnerabilities

List of Potential vulnerabilities
- unprotected MQTT Servers
	If the MQTT Server is not protected, then any data on it is unsecure. For our particular project, the only real threat from someone remotely accessing our system would be the ability to turn it off, but it is a good practice to password protect yout things.
	THREAT LEVEL RED
- unprotected MQTT Dashboard
	If the MQTT Dashboard is unprotected then anything you're tracking with it is unsecure and able to be interacted with by anyone who wants to. Our dashboard doesn't have anything on it that you could use to do any real harm to anyone, but again, IoT Security is pretty important.
	THREAT LEVEL REDDISH
- connected services that aren't password protected
	We are using Azure and Node Red to create our dashboard and systems so we are in the clear here, but if we didn't we would have a problem. Services and Apps that are connected to our IoT Device have the capability of opening up a backdoor into the system if we aren't careful about what we are trusting with our data
	THREAT LEVEL SOLID YELLOW
- be wary of third party applications
	I don't believe that we are using any third party apps at the moment, but it would be smart to think about the potential security flaws of another, unrelated application that we don't fully understand.
	THREAT LEVEL OPAQUE

PART 2 - Suggest solutions to security vulnerabilities
	Honestly so far most of the problems that we have identified specifically for our system involve a lack of passwords, so thats fairly easy to patch up with a bit of security work on our end.
