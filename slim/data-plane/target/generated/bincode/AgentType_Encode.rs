impl :: bincode :: Encode for AgentType
{
    fn encode < __E : :: bincode :: enc :: Encoder >
    (& self, encoder : & mut __E) ->core :: result :: Result < (), :: bincode
    :: error :: EncodeError >
    {
        :: bincode :: Encode :: encode(&self.organization, encoder) ?; ::
        bincode :: Encode :: encode(&self.namespace, encoder) ?; :: bincode ::
        Encode :: encode(&self.agent_type, encoder) ?; :: bincode :: Encode ::
        encode(&self.strings, encoder) ?; core :: result :: Result :: Ok(())
    }
}