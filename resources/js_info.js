const action = useCallback((fold, call, raise) => {
  if (fold) {
    sendJsonMessage({
      "MESSAGE TYPE": "ACTION",
      "MESSAGE": {
        "GAME_ID": "1",
        "PLAYER_NAME": "John Doe",
        "ACTION": "FOLD",
        "AMOUNT": "0"
      }
    })
    return;
  } else if (call) {
    sendJsonMessage({
      "MESSAGE TYPE": "ACTION",
      "MESSAGE": {
        "GAME_ID": "1",
        "PLAYER_NAME": "John Doe",
        "ACTION": "CALL",
        "AMOUNT": "0"
      }
    })
    return;
  } else if (raise) {
    sendJsonMessage({
      "MESSAGE TYPE": "ACTION",
      "MESSAGE": {
        "GAME_ID": "1",
        "PLAYER_NAME": "John Doe",
        "ACTION": "RAISE",
        "AMOUNT": bet
      }
    })
    setBet(0);
  }
})

const handleFold = async (event) => {
  event.preventDefault();

  try {
    action(true, false, false)
  } catch (err) {
    // error handle
  }
};

const handleCall = async (event) => {
  event.preventDefault();

  try {
    action(false, true, false)
  } catch (err) {
    // error handle
  }
};

const handleRaise = async (event) => {
  event.preventDefault();

  try {
    action(false, false, true)
  } catch (err) {
    // error handle
  }
};

const sitAtTable = useCallback(() => {
  sendJsonMessage({
    "MESSAGE TYPE": "JOIN",
    "MESSAGE": {
      "GAME_ID": "1",
      "PLAYER_NAME": "John Doe",
      "BALANCE": "100"
    }
  })
