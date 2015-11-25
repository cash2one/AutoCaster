//Win32 DLL hook for the League of Legends.exe process.
//Hooks Scaleform's Movie::Invoke() and Kernel32 OutputDebugStringA()
//Invoke hook is used to capture in-game events that are communicated to the flash UI
//OutputDebugStringA() is hooked to catch debug messages that indicate the end of a game
//Invoke address is hard coded for 5.23 (exe version 5.23.0.239)
 
//Hooked UI messages are sent via network socket to text-to-speech engine (AutoCaster uses python)
//To not block League "MAINLOOP" render loop during network send, send() is called on separate thread.
//Thread communication done via FIFO message queue.
 
//Injection can be done various ways. AutoCaster uses IAT insertion on the League of Legends.exe executable.
 
//Part of the AutoCaster Hackathon project.
 
#include <windows.h>
#include <vector>
#include <string>
#include <queue>
#include <thread>
 
using namespace std;
 
//Typedefs for functions we hook
typedef VOID  (__cdecl *INVOKE)(DWORD param1, DWORD function_name, DWORD symbol, DWORD data);
 
//Prototypes for custom hook functions.
VOID  __cdecl   CustomInvoke(DWORD param1, DWORD function_name, DWORD symbol, DWORD data);
VOID  __stdcall CustomOutputDebugStringA(_In_opt_ LPCSTR lpOutputString);
 
//Storage for bytes we lose by patching.
char lost_debug_bytes[10];
char lost_invoke_bytes[10];
 
//Addresses of hooked functions.
FARPROC OutputDebugStringAAddress;
FARPROC InvokeAddress;
 
//Prevent main entry point from being ran twice.
bool injected = false;
 
//Message Queue for multi-threaded sending to socket (python text-to-speech server)
std::queue<string>* message_queue = new std::queue<string>;
 
//Constants to ease opcode writing.
const byte MOV_EAX[] = { 0xb8 };
const byte JMP_EAX[] = { 0xff, 0xe0 };

//Offet for the Invoke method
const long INVOKE_OFFSET = 0x9627C0;
 
//======================================================================
 
//Functions to remove/apply hooks.
//Ideally we wouldn't be creating a new pair for each hook, but this way makes
//other future stuff easier. Pinky promise.
void ApplyOutputDebugStringAPatch(){
 
        //Save bytes we're about to overwrite.
        ReadProcessMemory(GetCurrentProcess(), OutputDebugStringAAddress, lost_debug_bytes, 10, 0);
 
        //Union to convert address to byte array
        union{
                byte arr[4];
                uintptr_t address;
        } tmp_union;
        tmp_union.address = reinterpret_cast<uintptr_t>(&CustomOutputDebugStringA);
 
        //Concat all bytes into a final vector.
        std::vector<byte> combined;
        for (int i = 0; i < sizeof(MOV_EAX); i++){
                combined.push_back(MOV_EAX[i]);
        }
        for (int i = 0; i < sizeof(tmp_union.arr); i++){
                combined.push_back(tmp_union.arr[i]);
        }
        for (int i = 0; i < sizeof(JMP_EAX); i++){
                combined.push_back(JMP_EAX[i]);
        }
 
        //Apply patch
        WriteProcessMemory(GetCurrentProcess(), OutputDebugStringAAddress, combined.data(), combined.size(), 0);
 
}
void RemoveOutputDebugStringAPatch(){
        WriteProcessMemory(GetCurrentProcess(), OutputDebugStringAAddress, lost_debug_bytes, sizeof(lost_debug_bytes), 0); //NEVER USED LOL
}
void ApplyInvokePatch(){
 
        //Save bytes we're about to overwrite.
        ReadProcessMemory(GetCurrentProcess(), InvokeAddress, lost_invoke_bytes, sizeof(lost_invoke_bytes), 0);
 
        //Union to convert address to byte array
        union{
                byte arr[4];
                uintptr_t address;
        } tmp_union;
        tmp_union.address = reinterpret_cast<uintptr_t>(&CustomInvoke);
 
        //Concat all bytes into a final vector.
        std::vector<byte> combined;
        for (int i = 0; i < sizeof(MOV_EAX); i++){
                combined.push_back(MOV_EAX[i]);
        }
        for (int i = 0; i < sizeof(tmp_union.arr); i++){
                combined.push_back(tmp_union.arr[i]);
        }
        for (int i = 0; i < sizeof(JMP_EAX); i++){
                combined.push_back(JMP_EAX[i]);
        }
 
        //Apply patch
        WriteProcessMemory(GetCurrentProcess(), InvokeAddress, combined.data(), combined.size(), 0);
}
void RemoveInvokePatch(){
        WriteProcessMemory(GetCurrentProcess(), InvokeAddress, lost_invoke_bytes, sizeof(lost_invoke_bytes), 0);
}
 
//Extract data from the invoke. Data can be narrow/wide strings, integers, floats...etc.
//We spend lots of time juggling wide/narrow strings here. Very important for "other" uses
//of Movie::Invoke() hooks.
VOID  __cdecl   CustomInvoke(DWORD param1, DWORD function_name, DWORD symbol, DWORD data){
 
        //Get the major function name. "Update" "UpdatePlayerDataIcons"...etc
        string narrow_function(reinterpret_cast<char*>(function_name));
        wstring wide_function(narrow_function.begin(), narrow_function.end());
 
        //Extract symbol
        string sym_string(reinterpret_cast<const char*>(symbol));
 
        //Extract the data paramater into a wide string, based on the symbol type.
        wstring wide_data;
 
        //Integer data
        if ("%d" == sym_string)
                wide_data = to_wstring(data);
 
        //char* (narrow string)
        else if (sym_string == "%s")
        {
                string tmp(reinterpret_cast<const char*>(data));
                wide_data = wstring(tmp.begin(), tmp.end());
        }
 
        //wchar_t*
        else if (sym_string == "%ls")
                wide_data = reinterpret_cast<const WCHAR*>(data);
 
        //Double
        else if (sym_string == "%f")
                wide_data = to_wstring((double)data);
 
        //Float
        else if (sym_string == "%hf")
                wide_data = to_wstring((float)data);
 
        //Undefined
        else if (sym_string == "%u")
                wide_data = L"undefined";
 
        //Exit if in-game messagebox is detected. Means game-over for multiple possible reasons.
        if (wide_data.find(L"messagebox") != string::npos)
                ExitProcess(0);
 
        //Make data a narrow string, add it to the message queue
        string narrow_data(wide_data.begin(), wide_data.end());
        string final_command("(" + narrow_function + ")" + narrow_data + "\n");
        message_queue->push(final_command);
 
        //Call the real InvokeAddress
        RemoveInvokePatch();
        ((INVOKE)InvokeAddress)(param1, function_name, symbol, data);
        ApplyInvokePatch();
 
}
VOID  __stdcall CustomOutputDebugStringA(_In_opt_ LPCSTR lpOutputString){
        string debug(lpOutputString);
        if (debug.find("Menu_GUI::SetEndOfGameVideoActive") != string::npos)
                ExitProcess(0);
}
 
//Used to add our dll to the IAT. Never called.
__declspec(dllexport) void Dummy(){
        return;
}
 
//Network loop that runs in it's own thread, sending
//queued messages to the text-to-speech python server.
void MessageSender(){
 
        //Init winsock, TCP socket, IP, port...etc
        WSADATA wsadata;
        int error = WSAStartup(0x0202, &wsadata);
        sockaddr_in target;
        target.sin_family = AF_INET;
        target.sin_port = htons(8444);
        target.sin_addr.s_addr = inet_addr("127.0.0.1");
        SOCKET scket = socket(AF_INET, SOCK_STREAM, IPPROTO_TCP);
        char value = 1;
        setsockopt(scket, IPPROTO_TCP, TCP_NODELAY, &value, sizeof(value));
 
        //Connect
        if (connect(scket, (SOCKADDR*)&target, sizeof(target)) == SOCKET_ERROR){
                MessageBox(NULL, L"Could not connect to text-to-speech server.", L"SOCKET ERROR", NULL);
                ExitProcess(0);
        }
 
        //Network loop. This can block without blocking GAMELOOP, no worries.
        while (1){
 
                //Wait for a message to appear
                if (message_queue->size() != 0){
 
                        //Get message to send from FIFO queue. And pop it off.
                        std::string message_to_send = message_queue->front();
                        message_queue->pop();
 
                        //Send it.
                        send(scket, message_to_send.c_str(), message_to_send.length(), 0);
 
                }
 
                Sleep(2);
        }
}
 
//Entry point. We apply all the needed hooks/patches here.
BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved)
{
 
        if (!injected){
 
                //Debugging stuff.
                AllocConsole();
                MessageBox(0, L"DLL ENTRY", L"DLL ENTRY", 0);
 
                //Block subsequent DLLMain calls.
                injected = true;
 
                //Hook debugoutput to catch end-of-game debug messages.
                HMODULE hKernel32 = GetModuleHandleA("kernel32.dll");
                OutputDebugStringAAddress = GetProcAddress(hKernel32, "OutputDebugStringA");
                ApplyOutputDebugStringAPatch();
 
                //Hook scaleform movie::invoke()
                HMODULE hBaseAddress = GetModuleHandle(L"League of Legends.exe");
                InvokeAddress = (FARPROC)((uintptr_t)hBaseAddress + INVOKE_OFFSET);
                ApplyInvokePatch();
 
                //Separate thread will send invoke messages to network socket, to not block hooked render loop.
                CreateThread(NULL, NULL, (LPTHREAD_START_ROUTINE)&MessageSender, NULL, NULL, NULL);
 
        }
 
        return true;
}
