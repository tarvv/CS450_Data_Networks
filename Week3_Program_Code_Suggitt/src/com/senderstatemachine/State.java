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
 * Hardcoded enum containing the states of the sender FSM
 */
public enum State {
    WAIT_CALL_0,
    WAIT_ACK_0,
    WAIT_CALL_1,
    WAIT_ACK_1
}
