impl :: bincode :: Encode for Agent
{
    fn encode < __E : :: bincode :: enc :: Encoder >
    (& self, encoder : & mut __E) ->core :: result :: Result < (), :: bincode
    :: error :: EncodeError >
    {
        :: bincode :: Encode :: encode(&self.agent_type, encoder) ?; ::
        bincode :: Encode :: encode(&self.agent_id, encoder) ?; core :: result
        :: Result :: Ok(())
    }
}