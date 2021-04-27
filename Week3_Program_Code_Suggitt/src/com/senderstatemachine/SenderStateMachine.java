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

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class SenderStateMachine {
    /* Constant declarations */
    static final State INITIALSTATE = State.WAIT_CALL_0;

    /**
     * Hard coded transition table for FSM. Format is: current state -> value of flags -> next state.
     * Flag values are decimal conversions of flags OR-ed together for the events in the provided FSM.
     */
    private static final int T_TABLE[][] = {
    //startState, eventFlags(decimal), toState
            {0, 1, 0},
            {0, 2, 1},
            {1, 4, 1},
            {1, 65, 1},
            {1, 9, 1},
            {1, 49, 2},
            {2, 1, 2},
            {2, 2, 3},
            {3, 4, 3},
            {3, 33, 3},
            {3, 9, 3},
            {3, 81, 0}
    };

    /**
     * Main method executes main program loop. Loop only exits on System.exit().
     * Maintains event flags and current state. Checks and performs transitions. Calls methods for handling actions, and
     * events and flag value math.
     *
     * @param args - command line arguments
     */
    public static void main(String[] args) {
        State currState = INITIALSTATE;
        int eventFlags = 0;
        boolean tFlag;
        System.out.println("Running sender FSM");
        System.out.println("Type \"Q\" at anytime to quit FSM");
        while(true) {
            tFlag = false;
            if (currState == State.WAIT_CALL_0 || currState == State.WAIT_CALL_1) {
                System.out.println("\nCurrent state: " + currState);
                eventFlags = callQuery();
            } else if (currState == State.WAIT_ACK_0 || currState == State.WAIT_ACK_1) {
                System.out.println("\nCurrent state: " + currState);
                eventFlags = ackQuery();
            } else {
                System.err.println("ERROR: Invalid state entered");
                System.err.println("PROGRAM EXITING");
                System.exit(1);
            }
            for (int i = 0; i < T_TABLE.length; i++) {
                if (T_TABLE[i][0] == currState.ordinal() && eventFlags == T_TABLE[i][1]) {
                    tFlag = true;
                    System.out.print("\nTransition: " + currState);
                    currState = State.values()[T_TABLE[i][2]];
                    System.out.println(" -> " + currState);
                    actionHandler(i);
                    break;
                }
            }
            if(tFlag == false) {
                System.out.println("No transition occurred. Sender is idle.");
            }
        }
    }

    /**
     * Queries user for events that occur while in states Wait Call 0 and Wait Call 1. Sets the corresponding event flag
     *
     * @return eventFlags - OR-ed value of events that user selected
     */
    public static int callQuery() {
        int eventFlags = 0;
        String userIn = "";
        BufferedReader r = new BufferedReader(new InputStreamReader(System.in));
        try {
            System.out.println("Type \"S\" to send a packet or \"R\" to request a packet");
            while(true) {
                userIn = r.readLine().toLowerCase();
                if (userIn.equals("q")) userShutDown();
                if (userIn.equals("r")) {
                    eventFlags |= Event.PACKET_REQUESTED.getFlag();
                    break;
                } else if (userIn.equals("s")) {
                    eventFlags |= Event.PACKET_RECEIVED.getFlag();
                    break;
                } else {
                    System.out.println("Must enter \"S\" or \"R\"");
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }

        return eventFlags;
    }

    /**
     * Queries user for events that occur while in states Wait ACK 0 and Wait ACK 1. Sets the corresponding event flag.
     *
     * @return eventFlags - OR-ed value of events that user selected
     */
    public static int ackQuery() {
        int eventFlags = 0;
        String userIn = "";
        BufferedReader r = new BufferedReader(new InputStreamReader(System.in));
        try {
            System.out.println("Type \"S\" to send a packet or \"T\" to simulate timer running out");
            while(true) {
                userIn = r.readLine().toLowerCase();
                if (userIn.equals("q")) userShutDown();
                if (userIn.equals("s")) {
                    eventFlags |= Event.PACKET_RECEIVED.getFlag();
                    System.out.println("Is packet an acknowledgement? \"Y\" or \"N\"");
                    while(true) {
                        userIn = r.readLine().toLowerCase();
                        if (userIn.equals("q")) userShutDown();
                        if (userIn.equals("y")) {
                            System.out.println("Which packet are you acknowledging? \"0\" or \"1\"");
                            while(true) {
                                userIn = r.readLine().toLowerCase();
                                if (userIn.equals("q")) userShutDown();
                                if (userIn.equals("0")) {
                                    eventFlags |= Event.ACK_0.getFlag();
                                    break;
                                } else if (userIn.equals("1")) {
                                    eventFlags |= Event.ACK_1.getFlag();
                                    break;
                                } else {
                                    System.out.println("Must enter \"1\" or \"0\"");
                                }
                            }
                            break;
                        } else if (userIn.equals("n")) {
                            break;
                        } else {
                            System.out.println("Must enter \"Y\" or \"N\"");
                        }
                    }
                    System.out.println("Is packet corrupt? \"Y\" or \"N\"");
                    while(true) {
                        userIn = r.readLine().toLowerCase();
                        if (userIn.equals("q")) userShutDown();
                        if (userIn.equals("y")) {
                            eventFlags |= Event.PACKET_CORRUPT.getFlag();
                            break;
                        } else if (userIn.equals("n")) {
                            eventFlags |= Event.PACKET_NOT_CURRUPT.getFlag();
                            break;
                        } else {
                            System.out.println("Must enter \"Y\" or \"N\"");
                        }
                    }
                    break;
                } else if (userIn.equals("t")) {
                    eventFlags |= Event.TIME_OUT.getFlag();
                    break;
                } else {
                    System.out.println("Must enter \"S\" or \"T\"");
                }
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return eventFlags;
    }

    /**
     * Handles actions that occur on transition. Action value represents a transition and is numbered by row in
     * transition table. Currently a framework with only informational lines printed and method names commented.
     *
     * @param action - int value row in transition table
     */
    public static void actionHandler(int action) {
        switch(action){
            case 0:
            case 3:
            case 4:
            case 6:
            case 9:
            case 10:
                System.out.println("Action: Throw packet away");
                break;
            case 1:
            case 7:
                //_snd_packet = make_pkt(0, data, checksum);
                //_udt_send(_snd_packet);
                //start_timer();
                System.out.println("Action: Make packet");
                System.out.println("Action: Send packet");
                System.out.println("Action: Reset timer");
                break;
            case 2:
            case 8:
                //_udt_send(_snd_packet);
                //start_timer();
                System.out.println("Action: Resend packet");
                System.out.println("Action: Reset timer");
                break;
            case 5:
            case 11:
                //stop_timer();
                System.out.println("Action: Stop timer");
                break;
            default:
                break;
        }
    }

    /**
     * Handles program shut down on user request.
     */
    public static void userShutDown() {
        System.out.println("Program is shutting down at user's request");
        System.exit(0);
    }
}
