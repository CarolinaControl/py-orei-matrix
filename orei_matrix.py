import asyncio
import logging

# --- CONFIGURATION ---
# Set your matrix IP address here (Static IP recommended)
HOST = "192.168.0.100"
PORT = 8000
TIMEOUT = 2  # Seconds

# Setup Logger
_LOGGER = logging.getLogger(__name__)

async def send_command(command_str):
    """
    Opens a connection, sends a command terminated by CR+LF,
    and returns the response.
    """
    reader = None
    writer = None
    response = ""
    
    try:
        # Connect to the Matrix
        reader, writer = await asyncio.open_connection(HOST, PORT)
        
        # Format command with CR LF 
        cmd = f"{command_str}\r\n"
        _LOGGER.info(f"Sending to OREI Matrix: {cmd.strip()}")
        
        writer.write(cmd.encode('ascii'))
        await writer.drain()

        # Read response (simple read with timeout)
        try:
            data = await asyncio.wait_for(reader.read(1024), timeout=TIMEOUT)
            response = data.decode('ascii').strip()
            _LOGGER.info(f"Received from OREI Matrix: {response}")
        except asyncio.TimeoutError:
            _LOGGER.warning("Timeout waiting for response from OREI Matrix")

    except Exception as e:
        _LOGGER.error(f"Error communicating with OREI Matrix: {e}")
    
    finally:
        if writer:
            writer.close()
            await writer.wait_closed()
            
    return response

@service
async def orei_set_route(input_id=None, output_id=None):
    """
    Routes Input (1-8) to Output(s). Use output_id=0 for ALL outputs.
    output_id can now be a single number or a list of numbers (e.g., [1, 2]).
    """
    if input_id is None or output_id is None:
        return

    # Ensure output_id is a list so we can loop through it
    if not isinstance(output_id, list):
        output_id = [output_id]

    # Loop through each output and send the command
    for out in output_id:
        cmd = f"set input {input_id} to {out}"
        await send_command(cmd)
        
        # Update state immediately for the UI
        if str(out) == "0":
            for i in range(1, 9):
                 state.set(f"sensor.orei_output_{i}", value=f"input_{input_id}")
        else:
            state.set(f"sensor.orei_output_{out}", value=f"input_{input_id}")
            
        # Tiny delay to prevent flooding the matrix with too many rapid commands
        await asyncio.sleep(0.2)


@service
async def orei_power(power_state=None):
    """
    Turns the Matrix ON or OFF.
    
    yaml example:
      service: pyscript.orei_power
      data:
        power_state: "on"
    """
    if power_state not in ["on", "off"]:
        _LOGGER.error("orei_power requires power_state to be 'on' or 'off'")
        return

    # Manual Command: power on / power off 
    cmd = f"power {power_state}"
    await send_command(cmd)
    state.set("switch.orei_power", value=power_state)


@service
async def orei_refresh_status():
    """
    Queries the matrix for the current source of all 8 outputs
    and updates Home Assistant entities.
    """
    # Loop through all 8 outputs
    for i in range(1, 9):
        # Manual Command: get output x source 
        cmd = f"get output {i} source"
        resp = await send_command(cmd)
        
        # Expected Response format: "HDMI out 1 video source HDMI 1" 
        if "video source HDMI" in resp:
            try:
                # Parse the input number from the end of the string
                parts = resp.split("HDMI")
                # The last part should be the input number (e.g., " 1")
                input_num = parts[-1].strip()
                
                # Update a sensor entity in Home Assistant
                entity_id = f"sensor.orei_output_{i}"
                state.set(entity_id, value=f"input_{input_num}")
                
            except Exception as e:
                _LOGGER.error(f"Error parsing status for output {i}: {e}")

@time_trigger('startup')
async def startup_sync():
    """Sync status on Home Assistant startup."""
    await orei_refresh_status()
