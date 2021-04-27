/**
 * SenderStateMachine simulates a FSM of a server sending data over a network and employs TCP style network
 * congestion control. The FSM is presented in ch3 of Computer Networking: A Top-Down Approach and Worldclass content.
 * Queries standard output for events then displays information such as current state, transitions caused by events,
 * and actions taken by sender
 *
 * Created for week 3 class assignment in CS450 at Regis University.
 *
 * @date 1/31/21
 * @author: Travis Suggitt
 */
package com.senderstatemachine;

/**
 * Hardcoded enum containing possible events. Values converted to binary for use as bit flags.
 * Line comments are corresponding methods that trigger event.
 */
public enum Event {
    PACKET_RECEIVED(1<<0),          //_rdt_rcvpkt(_rcv_packet)
    PACKET_REQUESTED(1<<1),         //_rdt_send(data)
    TIME_OUT(1<<2),                 //time_out
    PACKET_CORRUPT(1<<3),           //corrupt(_rcv_packet)
    PACKET_NOT_CURRUPT(1<<4),       //notcorrupt(_rcv_packet)
    ACK_0(1<<5),                    //isACK(_rcv_packet, 0)
    ACK_1(1<<6);                    //isACK(_rcv_packet, 1)

    /* Event value variable declaration */
    private final int flag;

    /* Event constructor */
    private Event(int flag) {
        this.flag = flag;
    }

    /**
     * Event value getter
     * @return flag - bitflag value of event
     */
    public int getFlag() {
        return this.flag;
    }
}
