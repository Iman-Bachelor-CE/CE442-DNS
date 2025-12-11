* **Overall goal of the session**

  * Design and implement a **VPN-like system in Python**.
  * Intercept **TCP traffic** on the client, **tunnel** it to a remote server with unrestricted internet, and forward it to the real destination.
  * The server sends responses back through the tunnel, and the client delivers them to local applications as if they came directly from the internet.

* **High-level data flow (conceptual VPN pipeline)**

  * On the **client**:

    * Capture outgoing **TCP packets** (not just raw data).
    * **Encapsulate** these packets inside another protocol (e.g. UDP, or even DNS packets) to bypass filtering.
    * Send the encapsulated packets to the **VPN server**.
  * On the **server**:

    * **Decapsulate** the received packets to recover the original TCP/IP packets.
    * Forward them to the **real destination** on the open internet.
    * Receive the responses from the destination.
    * **Re-encapsulate** the response packets and send them back to the client.
  * Back on the **client**:

    * Decapsulate responses.
    * Inject the resulting packets so that local applications receive them as if they came directly from the network.

* **Why a simple socket approach is not enough**

  * A normal Python TCP socket only exposes the **payload** (application data), not:

    * IP addresses (source/destination).
    * TCP headers and flags.
    * Parameters like MSS, window size, etc.
  * For a real VPN-style tunnel, you need access to the **full packet**:

    * Ethernet frame → IP header → TCP header → data.

* **Packet sniffing and its limitations**

  * A typical **packet sniffer** (like Wireshark or a raw-socket sniffer) sits on a **network interface** and reads Ethernet frames.
  * Using a sniffer in parallel with the normal OS networking stack causes conflicts:

    * The **kernel/OS** is still handling packets normally.
    * Your **VPN code** is also reading the same packets and potentially sending alternative responses.
  * Example conflict:

    * The OS sends a request to a blocked site.
    * The filtered path returns an HTTP 403 (blocked).
    * The VPN tunnel returns the “real” response from the open internet.
    * Whichever response reaches the application first might “win,” causing **race conditions and broken connections**.

* **Understanding network interfaces in this context**

  * Running `ip a` (or similar) shows multiple interfaces:

    * `lo` (loopback interface).
    * Physical interfaces (e.g. Wi-Fi card).
    * Existing VPN interfaces (e.g. from Outline or other VPNs).
    * Bridge interfaces for virtual machines, containers, etc.
  * Key points:

    * These interfaces operate at **Layer 2 (Ethernet)**.
    * Packet sniffers attach to a specific interface and read **Ethernet frames**.
    * From each frame you can parse:

      * Ethernet header → IP header → TCP/UDP header → payload.

* **Why we need our *own* virtual interface**

  * Goal: ensure **all targeted traffic passes exclusively through our code**, not through the OS network stack in parallel.
  * If we only sniff on an existing interface:

    * The OS still receives and processes the packets.
    * We cannot reliably prevent the OS from sending its own responses.
  * Solution idea:

    * Create a **virtual network interface** whose packet I/O is completely controlled by our user-space program.
    * Configure routing so that traffic we care about goes through that virtual interface.

* **TUN/TAP on Linux (core mechanism)**

  * Linux provides **TUN/TAP devices** as a kernel feature:

    * They appear as normal network interfaces (visible in `ip a`).
    * But behind them, instead of a physical NIC, there is a **user-space program**.
  * Two flavors conceptually:

    * **TUN**: virtual **IP** device (works with IP packets).
    * **TAP**: virtual **Ethernet** device (works with full Ethernet frames).
  * How they behave:

    * When the OS sends a packet “to the network” via this interface:

      * The packet is not sent to hardware; it is delivered to your **program** via a file descriptor.
    * When your program writes a packet to the TUN/TAP device:

      * The kernel injects it into the networking stack as if it came from a real interface.
  * This is exactly what a VPN implementation needs:

    * OS sees a normal network interface.
    * All traffic routed through it is actually handled by your code.

* **Using TUN for the custom VPN**

  * **On the client:**

    * Create a **TUN interface** via the TUN/TAP API.
    * Configure IP and routing so that desired traffic (e.g. all, or some subnets) goes through this TUN interface.
    * Your Python program:

      * Reads IP packets from the TUN device.
      * Encapsulates them (e.g. in UDP/DNS).
      * Sends them to the VPN server.
      * Receives encapsulated responses from the server.
      * Decapsulates them and writes the resulting IP packets **back into the TUN interface**.
  * **On the server:**

    * Receive encapsulated packets.
    * Decapsulate to obtain original IP/TCP packets.
    * Forward them to the actual destination using normal sockets or raw packet injection.
    * Capture the responses and send them back through the tunnel in the reverse direction.

* **Why this avoids the earlier conflicts**

  * The **OS networking stack** is configured to send traffic through the TUN interface.
  * Your **program** is the only path between:

    * The OS/networking stack.
    * The external internet.
  * There is no “competition” between:

    * A filtered direct path, and
    * The VPN tunnel,
      because traffic to those destinations is no longer going out via the physical interface directly.

* **Planned implementation steps (as described in the voice note)**

  * Start a **new project** dedicated to this VPN experiment.
  * In code:

    * Create and configure a **TUN device**.
    * Verify that it appears as a network interface (e.g. via `ip a`).
    * Set up IP and routing so traffic flows through it.
    * Implement the logic to:

      * Read raw IP packets from the TUN device.
      * Encapsulate and send them to the VPN server.
      * Receive and decapsulate responses.
      * Write the resulting packets back to the TUN device.
  * Build this **step by step**, testing each stage (interface creation, routing, packet I/O, tunneling) as they go.
